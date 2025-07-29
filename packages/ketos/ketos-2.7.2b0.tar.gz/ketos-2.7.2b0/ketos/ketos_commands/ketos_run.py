import pickle
import pandas as pd
import os
import yaml
import numpy as np
import sys
import warnings
from ketos.ketos_commands.constants import EXIT_ERROR, EXIT_INTERRUPTION, EXIT_SUCCESS
from pathlib import Path
from ketos.ketos_commands.ketos_logger import KetosLogger


def _ketos_run_output_function(batch_detections, output_folder, mode, threshold=0.5, merge_detections=False, buffer=None, running_avg=None, labels=None, highest_score_only=False, **output_function_arguments):
    """ Converts network raw output into detection data.

        This function processes the output of a network into user-friendly detection data, 
        which is then saved to a .csv file. By default, each detection instance is stored 
        as a separate line in the .csv file.

        While this function offers a default conversion method, it can be overwritten to suit 
        specific use cases, transforming the network output based on user requirements.

        The contents of the network output batch (batch_detections) will 
        vary depending on the type of network. The format of batch_detections for various types of classifiers are as follows:

        Binary Classifier:

        {
         'filename': ['file1.wav', 'file1.wav', 'file1.wav'], 
         'start': [0.0, 3.0, 6.0], 
         'end': [3.0, 6.0, 9.0], 
         'score': [[0.3, 0.7], [0.8, 0.2], [0.1, 0.9]]
        }

        Multiclass Classifier:

        {
         'filename': ['file1.wav', 'file1.wav', 'file1.wav'], 
         'start': [0.0, 3.0, 6.0], 
         'end': [3.0, 6.0, 9.0], 
         'score': [[0.3, 0.6, 0.1], [0.6, 0.2, 0.2], [0.3, 0.4, 0.3]]
        }

        Sequence Classifier:

        {
         'filename': ['file1.wav'],
         'start': [0.0],
         'end': [10.0],
         'score': [[
             [0.8, 0.9, 0.7, 0.2, 0.1, 0.6, 0.9, 0.9, 0.2, 0.6],
             [0.7, 0.4, 0.6, 0.8, 0.6, 0.7, 0.8, 0.6, 0.1, 0.5]
         ]]
        }

        Args:
            batch_detections: dict
                A dictionary containing network outputs, including "filename", "start", "end", and "score" fields.
            output_folder: str
                The path to the folder where the output .csv file will be saved.
            mode: str
                The file I/O mode to be used while writing the .csv file. Typically 'w' for write or 'a' for append.
            threshold: float
                The score threshold for filtering detections. Defaults to 0.5.
            merge_detections: bool
                If True, overlapping detections will be merged into single detections. Defaults to False.
            buffer: float
                Adds buffer (seconds) to the start and end times of each detection. Defaults to None.
            running_avg: float
                If set, computes the running average of scores over the provided window. Defaults to None.
            labels: list or integer 
                A list of labels to filter by. Defaults to None
            highest_score_only: boolean
                If True, will only return the label associated with the highest score even if more than one passes the threshold. Defaults to False.
            output_function_arguments: dict
                Additional keyword arguments for the function.
    """    
    from ketos.neural_networks.dev_utils.detection import convert_sequence_to_snapshot, add_detection_buffer, merge_overlapping_detections, filter_by_threshold, filter_by_label, compute_score_running_avg

    if running_avg is not None:
        batch_detections['score'] = compute_score_running_avg(batch_detections['score'], running_avg)
    

    if batch_detections['score'].ndim == 2: # snapshot
        batch_detections = filter_by_threshold(batch_detections, threshold, highest_score_only)
    else: # sequence model
        batch_detections = convert_sequence_to_snapshot(batch_detections, threshold)

    if labels is not None:
        batch_detections = filter_by_label(batch_detections, labels)

    if merge_detections:
        batch_detections = merge_overlapping_detections(batch_detections)

    if buffer is not None:
        batch_detections = add_detection_buffer(batch_detections, buffer)

    header = True if mode == "w" else False
    output = (output_folder / "detections.csv")

    if not batch_detections.empty:
        batch_detections.to_csv(output, mode=mode, index=False, header=header)
    elif mode == 'w' or not output.exists():
        # If batch_detections is empty and mode is 'w', write an empty DataFrame to the file.
        empty_df = pd.DataFrame(columns=['filename', 'start', 'end', 'label', 'score'])
        empty_df.to_csv(output, mode='w', index=False, header=header)


def get_last_processed_batch(log_file):
    """
    Reads the log file, extracts the last processed batch number and returns it.

    This function is designed to recover the state of a process in case of an
    interruption or crash. It opens the log file and reads the log entries
    in reverse order, looking for the most recent 'Step' entry. It then 
    parses this entry to extract the batch number, which it returns.

    The function also handles two special cases: 
    1. If the log file does not exist (indicating that no batches have been 
       processed), it returns -1.
    2. If the last line in the log file is 'Process finished successfully', 
       it returns None. This is to indicate that the process was completed 
       successfully and does not need to be resumed.

    Parameters:
        log_file (str): Path to the log file.

    Returns:
        int, None: The number of the last processed batch, or None if the 
               process finished successfully.
    """

    last_processed_batch = -1
    try:
        with open(log_file, 'r') as f:
            docs = yaml.load_all(f, Loader=yaml.SafeLoader)

            for doc in docs:
                if 'step' in doc:
                    last_processed_batch = doc.get('step')
                elif doc.get('event').startswith('Process finished.'):
                    last_processed_batch = None

    except FileNotFoundError:
        # Log file doesn't exist, no batches have been processed
        warnings.warn(
            "Overwrite is set to False, but no existing log file was found to resume processing. The process will start from the beginning.",
            category=UserWarning
        )
        return -1
    return last_processed_batch

def _get_num_batches_from_hdf5(hdf5_file_path, batch_size, table_name=None):
    """ Helper function to return the number of batches in an HDF5 file."""
    import tables
    if table_name is None:
        table_name = "/data"
    else:
        table_name = table_name + "/data"

    with tables.open_file(hdf5_file_path, 'r') as hdf5_file:
        table = hdf5_file.get_node(table_name)
        num_samples = table.shape[0]
        num_batches = int(np.ceil(num_samples / batch_size))

    return num_batches 

def ketos_run(
        model_file, 
        audio_data, 
        file_list=None, 
        table_name=None, 
        output_folder=None, 
        overwrite=True, 
        log_file="ketos-run.log", 
        step_size=None, 
        batch_size=32, 
        threshold=0.5, 
        labels=None, 
        merge_detections=False, 
        buffer=None, 
        running_avg=None, 
        highest_score_only=False, 
        output_function_arguments=None):
    """ 
    Executes a model on given audio data and logs the process.

    This function handles loading and running a machine learning model trained
    with Ketos. It can operate on either a single audio file, a list of files,
    or an entire directory. The function logs its progress, including which
    audio files have been processed, and can resume from where it left off
    in the event of an interruption.

    Args:
        model_file: str
            Path to the .kt file containing the trained model.
        audio_data: str
            Path to the audio data to be processed. This can be a path to a single audio file, a directory of audio files, or an HDF5 database.
        file_list: str
            Path to a CSV file containing a list of specific files to be processed. Defaults to None.
        table_name: str
            Name of the table in the hdf5 file, if applicable. Defaults to None.
        output_folder: str
            Directory where the output will be saved. If not specified, defaults to current directory.
        overwrite: bool
            Whether to overwrite existing files. Defaults to True.
        log_file: str
            Name of the log file. Defaults to "ketos-run.log".
        step_size: float
            Size of the step for the audio frame loader. If not specified, set to the duration of the audio representation.
        batch_size: int
            Size of the data batches that the model will process. Defaults to 32.
        threshold: float
            Threshold for classifying detections. Defaults to 0.5.
        labels: list or integer 
                A list of labels to filter by. Defaults to None
        merge_detections: bool
            Whether to merge detections in output. Defaults to False.
        buffer: int
            Buffer to be added to start and end of each detection. Defaults to None.
        running_avg: float
            Exponential decay factor to compute the running average of detections. Defaults to None.
        highest_score_only: boolean
            If True, will only return the label associated with the highest score even if more than one passes the threshold. Defaults to False.
        output_function_arguments: dict
            Additional arguments to be passed to the output function. Defaults to None.
    """

    from ketos.audio.audio_loader import AudioFrameLoader
    from ketos.audio import load_audio_representation_from_file
    from ketos.neural_networks import load_model_file, load_input_transform_function, load_export_transform_function
    from ketos.neural_networks.dev_utils.detection import batch_load_audio_file_data, batch_load_hdf5_data

    if output_function_arguments is None:
        output_function_arguments = {}

    output_function_arguments.update({
        'threshold': threshold,
        'labels': labels,
        'merge_detections': merge_detections,
        'buffer': buffer,
        'running_avg': running_avg,
        # add any other optional arguments here
    })

    if output_folder is None:
        output_folder = Path('.').resolve()
    else:
        output_folder = Path(output_folder).resolve()
    
    output_folder.parent.mkdir(parents=True, exist_ok=True)

    mode = "w"
    last_processed_batch = -1
    if not overwrite:
        mode = "a"

        log_file_path = output_folder / log_file
        last_processed_batch = get_last_processed_batch(log_file_path)
        if last_processed_batch is None:
            print("There are no more files to process.")
            return

    # load the model from the .kt file
    model = load_model_file(model_file, load_audio_repr=False) 
    
    # load the audio representation from the .kt file
    audio_representation = load_audio_representation_from_file(model_file)

    # Currently the script only works with one audio representation
    audio_representation_name, audio_representation = next(iter(audio_representation[0].items()))

    # Try to load input transform function from model file. Otherwise try to load the one defined on the model, otherwise there is none
    try:
        input_transform_func = load_input_transform_function(model_file)
        # Warn the user about using a custom input transform function
        warnings.warn("Ketos detected a custom input function and will be using that.", UserWarning)
    except (AttributeError, ImportError):
        try:
            input_transform_func = model._transform_input
        except:
            input_transform_func = None
    # if step size was not specified, set it equal to the window size
    if step_size is None:
        step_size = audio_representation['duration']

    output = (output_folder / "raw_output.pkl")

    
    #  try to load from the model file. Otherwise load the default one
    try:
        output_function = load_export_transform_function(model_file)
        # Warn the user about using a custom input transform function
        warnings.warn("Ketos detected a custom output function and will be using that.", UserWarning)
    except AttributeError:
        output_function = _ketos_run_output_function
    
    audio_path = Path(audio_data)

    # Check if audio_data is a folder (thereby containing wav files) or an hdf5 database
    if audio_path.is_file():
        if audio_path.suffix == '.h5':
            # is hdf5
            batch_generator = lambda: batch_load_hdf5_data(
                                        hdf5_file_path=audio_path, 
                                        batch_size=batch_size, 
                                        audio_representation=audio_representation, 
                                        start_idx=last_processed_batch+1, 
                                        table_name=table_name, 
                                        x_field=audio_representation_name, 
                                        logger=logger
                                        )
            
            n_steps = _get_num_batches_from_hdf5(hdf5_file_path=audio_path, batch_size=batch_size, table_name=table_name)
    
        elif audio_path.suffix == '.wav':
            # is a single audio file
            audio_files = [audio_path]

            # initialize audio loader for a single file
            loader = AudioFrameLoader(duration=audio_representation["duration"], pad=False, step=step_size, batch_size=1,
                                    filename=audio_files, representation=audio_representation['type'], representation_params=audio_representation)

            n_steps = int(np.ceil(loader.num() / batch_size))

            batch_generator = lambda: batch_load_audio_file_data(loader=loader, batch_size=batch_size, start_idx=last_processed_batch+1, logger=logger)
        else:
            raise ValueError("Unsupported file type. Only '.h5' and '.wav' files are supported.")
    else:
        # is an audio folder
        # recursively getting a list of all files in folder that ends with .wav
        audio_files = [audio_file for audio_file in audio_path.rglob('*.wav')]

        if file_list is not None:
            file_list = pd.read_csv(file_list, header=None)[0].values.tolist()
            # filtering all the files paths to only process the ones we specified in file_list
            audio_files = [row for row in audio_files if row.rsplit(os.sep,1)[1] in file_list] 
    
        # initialize audio loader
        # The audio loader will segment an audio recording into segments of size "duration"
        # This is a generator that yields each segment as a spectrogram
        loader = AudioFrameLoader(duration=audio_representation["duration"], pad=False, step=step_size, batch_size=1,
            filename=audio_files, representation=audio_representation['type'], representation_params=audio_representation)

        n_steps = int(np.ceil(loader.num() / batch_size))

        batch_generator = lambda: batch_load_audio_file_data(loader=loader, batch_size=batch_size, start_idx=last_processed_batch+1, logger=logger)

    logger = KetosLogger('ketos-run', str(Path(output_folder, log_file)), mode=mode, format='yaml')

    # Log the initial parameters
    logger.info("Process started", stdout=True, **{
        'parameters': {
            'model_file': model_file,
            'audio_data': audio_data,
            'file_list': file_list,
            'table_name': table_name,
            'output_folder': str(output_folder),
            'overwrite': overwrite,
            'log_file': log_file,
            'step_size': step_size,
            'batch_size': batch_size,
            'threshold': threshold,
            'merge_detections': merge_detections,
            'buffer': buffer,
            'running_avg': running_avg,
            'highest_score_only': highest_score_only,
            'output_function_arguments': output_function_arguments,
        },
        'n_steps': n_steps,
        'status': 'success'
    })

    filenames = None
    try:
        # the arguments for the chosen generator function have already been passed by the lambda function
        for idx, batch_data in enumerate(batch_generator(), start=last_processed_batch+1):
            successful_process = False
            try:
                filenames = list(dict.fromkeys(str(path) for path in batch_data['filename'])) # getting the unique elements and converting path object to str

                # if input_transform_func is not None:
                #     data = input_transform_func(batch_data['data'], training=False)
                
                batch_predictions = model.run_on_batch(batch_data['data'], input_transform_function=input_transform_func, output_transform_function=None) 
                # batch_predictions = model.model.predict_on_batch(data)

                raw_output = {'filename': batch_data['filename'], 'start': batch_data['start'], 'end': batch_data['end'], 'score': batch_predictions}

                with open(output, mode+'b') as f:
                    pickle.dump(raw_output, f)

                # Run the output transform function. The user can customize this function
                output_function(raw_output, output_folder, mode, **output_function_arguments)
                successful_process = True # <-- SET FLAG TO TRUE AFTER SUCCESSFUL PROCESS. We need this flag for when we interrupt the process after successful completion but before the next batch starts
                mode = "a"

                logger.info(f"Step {str(idx)}", **{
                    'step': idx,
                    'files': filenames,
                    'status': 'success'
                })

            except Exception as e:
                if successful_process:
                    idx += 1 # Set to the next index because
                logger.error(f'{e}', stdout=True, **{'status': 'error'})
                raise

    except KeyboardInterrupt as e:
        if filenames is not None:
            if successful_process:
                idx += 1 # Set to the next index because
            logger.error('Process was interrupted by user.', stdout=True, **{
                'step': idx,
                'files': filenames,
                'status': 'interruption'
            })
        raise
    else:
        # This block executes only if the loop completed without encountering a break statement.
        logger.info(f"Process finished. Output saved to: {output_folder}", stdout=True, **{
            'output': {
                'folder': str(output_folder)
            },
            'status': 'success'
        })


def main():
    import argparse
    import warnings
    import ast
    def boolean_string(s):
            if s not in {'False', 'True'}:
                raise ValueError('Not a valid boolean string')
            return s == 'True'

    def tryeval(val):
        # Literal eval does cast type safely. However, doesnt work for str, therefore the try except.
        try:
            val = ast.literal_eval(val)
        except ValueError:
            pass
        return val
        
    class ParseKwargs(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            setattr(namespace, self.dest, dict())
            for value in values:
                key, value = value.split('=')
                getattr(namespace, self.dest)[key] = tryeval(value)

    # parse command-line args
    parser = argparse.ArgumentParser()
    parser.add_argument('model_file', type=str, help='Path to the ketos model file (*.kt)')
    parser.add_argument('audio_data', type=str, help='Path to the audio data to be processed. This can be a path to a single audio file, a directory of audio files, or an HDF5 database.')
    parser.add_argument('--file_list', default=None, type=str, help='A .csv or .txt file where each row (or line) is the name of a file to detect within the audio folder. \
                        By default, all files will be processed. Not relevant if audio_data is an HDF5 file.')
    parser.add_argument('--table_name', default=None, type=str, help="Table name within the HDF5 database where the data is stored. Must start with a foward slash. For instance '/test'. \
                        If not given, the root '/' path will be used. Not relevant if audio_data is a fodler with audio files.")
    parser.add_argument('--output_folder', default=None, type=str, help='Location to output the detections. For instance: detections/')
    parser.add_argument('--overwrite', default=True, type=boolean_string, help='Overwrites the detections, otherwise appends to it.')
    parser.add_argument('--log_file', default="ketos-run.log", type=str, help='Name of the log file to be created/used during the process. Defaults to "ketos-run.log".')
    parser.add_argument('--step_size', default=None, type=float, help='Step size in seconds. If not specified, the step size is set equal to the duration of the audio representation.')
    parser.add_argument('--threshold', default=0.5, type=float, help="The threshold value used to determine the cut-off point for detections. This is a floating-point value between 0 and 1. A detection is considered positive if its score is above this threshold. The default value is 0.5.")
    parser.add_argument('--labels', type=tryeval, default=None, help="List or integer of labels to filter by. Example usage: --labels 1 or --labels [1,2,3]. Defaults to None.")
    parser.add_argument('--merge_detections', default=False, type=boolean_string, 
                    help="A flag indicating whether to merge overlapping detections into a single detection. If set to True, overlapping detections are merged. The default value is False, meaning detections are kept separate.")
    parser.add_argument('--buffer', default=0.0, type=float, 
                    help="The buffer duration to be added to each detection in seconds. This helps to extend the start and end times of each detection to include some context around the detected event. The default value is 0.0, which means no buffer is added.")
    parser.add_argument('--running_avg', default=None, type=int, 
                    help="Compute a running average of the scores over a specified window size in frames. Must be an odd integer.")
    parser.add_argument('--highest_score_only', default=False, type=boolean_string,
                    help='If True, will only return the label associated with the highest score even if more than one passes the threshold. Defaults to False.')
    parser.add_argument('--batch_size', default=32, type=int, help='How many samples will be loaded into memory. Lower this number if you are running into out of memory problems.')
    parser.add_argument('--output_function_arguments', default=None, nargs='*', action=ParseKwargs, help='Output function arguments. If you created a custom output transform function, you can \
        use this option to pass any arguments to it. Usage: --output_function_arguments arg1=value1 arg2=value2')

    try:
        args = parser.parse_args()
        ketos_run(**vars(args))

    except KeyboardInterrupt:
        print("Program was interrupted by the user.")
        sys.exit(EXIT_INTERRUPTION)

    else:
        sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()