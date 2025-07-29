import numpy as np
import yaml
import json
import pandas as pd
import random
import tables as tb
import os
from ketos.audio.audio_loader import AudioLoader, SelectionTableIterator
from tqdm import tqdm
from pathlib import Path
from ketos.data_handling.annotations_handling import standardize, adjust_segment_interval, generate_time_shifted_segments, create_random_segments
from ketos.data_handling.data_handling import file_duration_table
from ketos.data_handling.hdf5_interface import generate_table_description, insert_representation_data, create_table
from ketos.data_handling.parsing import load_audio_representation

def load_config(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        try:
            return json.loads(content)  # Try JSON first
        except json.JSONDecodeError:
            return yaml.safe_load(content)  # Then try YAML

def create_db(data_dir, 
              audio_representation, 
              annotations=None, 
              annotation_step=0, 
              step_min_overlap=0.5, 
              labels=None, 
              output=None, 
              table_name=None, 
              random_selections=None, 
              avoid_annotations=None, 
              overwrite=False, 
              seed=None, 
              only_augmented=False, 
              custom_module=None
              ):
    """
    custom_module: Directory containing custom components like neural network architectures and transformation functions. Defaults to None.
    """
    
    # Initialize random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    # Raise an exception if both annotations and random_selections are None
    if random_selections is None and annotations is None:
        raise Exception("Missing value: Either annotations or random_selection must be defined.")
    
    # Open and read the audio configuration file (e.g., JSON file with audio settings)
    # config = load_config(audio_representation)[0]

    if custom_module:
        custom_module = Path(custom_module)
    
    # 
    # print(type_value)
    representation_class_module_path = custom_module / "audio_representation.py" if custom_module else None
    config = load_audio_representation(audio_representation, module_path=representation_class_module_path)
    representation_name = list(config.keys())[0]
    config = config[representation_name]
    representation_class = config.pop("type", None)
    # representation_class = import_audio_representation(name=type_value, module_path=str(representation_class_module_path) if representation_class_module_path else None)
    ####### VERY IMPORTANT!!!
    # We need to remove the parsing from the audio representations eventually


    selections = {}

    annots = None
    
    print('Extracting files durations')
    files = file_duration_table(data_dir, num=None)

    # Creating a dictionary for quick and easy lookup and access: {filename: duration}
    file_durations = dict(zip(files["filename"], files["duration"]))

    if annotations is not None: # If an annotation table is provided
        annots = pd.read_csv(annotations)
        annots = standardize(annots, labels=labels) # Standardize annotations by mapping labels to integers
        
        # Get the list of labels after processing
        labels = annots.label.unique().tolist()
   
        # Remove any label equal to -1 (an "ignore" label)
        labels = [label for label in labels if label != -1]

        # Check if start and end times are present in the annotation dataframe
        if 'start' in annots.columns and 'end' in annots.columns:
            for label in labels:
                # Define segments for the given label based on annotation data
                selections[label] = adjust_segment_interval(annots, duration=config['duration'], center=True)

                # If annotation_step is set, create time-shifted instances("
                if annotation_step > 0:
                    shifted_segments = generate_time_shifted_segments(selections[label], step=annotation_step, min_overlap=step_min_overlap, include_unshifted=False)
                    
                    if only_augmented:
                        # Only include the time-shifted segments and discard the original ones
                        selections[label] = shifted_segments
                    else:
                        # Concatenate the original segments with the new time-shifted instances
                        selections[label] = pd.concat([selections[label], shifted_segments], ignore_index=True)

                # Filter out invalid annotations
                selections[label] = selections[label][
                    (selections[label]['start'] >= 0) &  # Start time must be non-negative
                    (selections[label].apply(lambda row: row['end'] <= file_durations.get(row['filename'], float('inf')), axis=1))  # End time must be within file duration
                ]
        else:
            # If start and end are not present, treat annotations as selections directly 
            for label in labels:
                selections[label] = annots.loc[annots['label'] == label]

    # Generating new random segments
    if random_selections is not None: 
        num_segments = random_selections[0] # Number of segments to generate
        if avoid_annotations is not None and annotations is None: # Avoid areas with existing annotations
            annots = pd.read_csv(avoid_annotations)
            annots = standardize(annots, labels=labels)
            
            if num_segments == 'same':
                raise ValueError("The number of background samples to generate cannot be 'same' when avoid_annotations is being used.")

        if num_segments == 'same': # If num_segments is 'same', generate as many samples as the largest selection
            biggest_selection = float('-inf') 
            for label in labels:
                if len(selections[label]) > biggest_selection:
                    biggest_selection = len(selections[label])

            num_segments = biggest_selection

        print(f'\nGenerating {num_segments} samples with label {random_selections[1]}...')

        # If filenames are provided, filter the file list based on them
        if random_selections[2]:
            with open(random_selections[2], 'r') as file:
                filenames = file.read().splitlines()
            files = files[files['filename'].isin(filenames)]
        
        # Generate random segments based on the file durations and label
        rando = create_random_segments(files, config['duration'], num_segments, label=random_selections[1], annotations=annots)
        
        if labels is None:
            labels = []
            
        if random_selections[1] in labels: 
            # if the random selection label already exists in the selections, concatenate the generatiosn with the selections that already exist
            selections[random_selections[1]] = pd.concat([selections[random_selections[1]], rando], ignore_index=False) # concatenating the generated random selections with the existings selections
        else:
            # if the random selections label did not yet exist in the selections, add it to the list of labels
            labels.append(random_selections[1])
            selections[random_selections[1]] = rando

    if output is None:
        output = "create_db_dir/db.h5"
    output = Path(output)

    # Ensure output is an absolute path
    if not output.is_absolute():
        output = Path.cwd() / output

    # Create the directory if it doesn't exist
    output.parent.mkdir(parents=True, exist_ok=True)

    if overwrite and output.exists():
        output.unlink()
            
    print('\nCreating HDF5 db...')
    with tb.open_file(output, mode='a') as h5file:
        first_key = labels[0]
        start = 0
        if 'start' in selections[first_key].iloc[0].index:
            start = selections[first_key].iloc[0]['start']
        # Load the first sample to determine the table shape
        seg = representation_class.from_wav(path=str(Path(data_dir) / selections[first_key].iloc[0]['filename']), offset=start, **config).data
        table = create_table(h5file, table_name, generate_table_description(seg, representation_name), table_name='data')

        # Loop through each label and add its data to the table
        for label in labels:
            print(f'\nAdding data with label {label} to table {table_name} with shape {seg.shape}...')
            selections_label = selections[label]

            # loader = AudioLoader(selection_gen=SelectionTableIterator(data_dir=data_dir, 
            #     selection_table=selections, include_attrs=include_attrs, 
            #     attrs=attrs), channel=channel, annotations=annotations, representation=representation, representation_params=representation_params)

            for _, row in tqdm(selections_label.iterrows(), total=selections_label.shape[0]):
                start = 0
                if 'start' in row.index:
                    start = row['start']

                file_path = os.path.join(data_dir, row['filename'])
                representation_data = representation_class.from_wav(path=file_path, offset=start, **config).data
                
                # Insert spectrogram data into the table
                insert_representation_data(table, row['filename'], start, label, representation_data, representation_name=representation_name)                  


def main():
    import argparse

    def boolean_string(s):
        if s not in {'False', 'True'}:
            raise ValueError('Not a valid boolean string')
        return s == 'True'

    class ParseKwargs(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if len(values) == 1 and not '=' in values[0]:  # Single value
                setattr(namespace, self.dest, [int(values[0])] if values[0].isdigit() else [values[0]])
            elif not any('=' in value for value in values):  # List of values
                setattr(namespace, self.dest, [int(val) if val.isdigit() else val for val in values])
            else:  # Key-value pairs
                kwargs = {}
                for value in values:
                    if '=' not in value:
                        parser.error(f"Invalid format for {option_string}: expected key=value but got '{value}'")
                    key, val = value.split('=')
                    if val.isdigit():
                        val = int(val)
                    kwargs[key] = val
                setattr(namespace, self.dest, kwargs)
                
    class RandomSelectionsAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if len(values) < 2:
                parser.error("--random_selections requires at least two arguments")
            x = values[0] if values[0] == 'same' else int(values[0])
            y = int(values[1])
            z = values[2] if len(values) > 2 else None
            setattr(namespace, self.dest, (x, y, z))

    # parse command-line args
    parser = argparse.ArgumentParser()
    parser.add_argument('data_dir', type=str, help='Path to the directory containing the audio files')
    parser.add_argument('audio_representation', type=str, help='Path to the audio representation config file')
    parser.add_argument('--annotations', default=None, type=str, help='Path to the annotations .csv')
    parser.add_argument('--annotation_step', default=0, type=float, help='Produce multiple time shifted representations views for each annotated  section by shifting the annotation  \
                window in steps of length step (in seconds) both forward and backward in time. The default value is 0.')
    parser.add_argument('--step_min_overlap', default=0.5, type=float, help='Minimum required overlap between the annotated section and the representation view, expressed as a fraction of whichever of the two is shorter. Only used if step > 0.')
    parser.add_argument('--labels', default=None, nargs='*', action=ParseKwargs, help='Specify a label mapping. Example: --labels background=0 upcall=1 will map labels with the string background to 0 and labels with string upcall to 1. \
        Any label not included in this mapping will be discarded. If None, will save every label in the annotation csv and will map the labels to 0, 1, 2, 3....')
    parser.add_argument('--table_name', default=None, type=str, help="Table name within the database where the data will be stored. Must start with a foward slash. For instance '/train'")
    parser.add_argument('--random_selections', default=None, nargs='+', type=str, action=RandomSelectionsAction, help='Will generate random x number of samples with label y. By default, all files in the data_dir and subdirectories will be used.  \
                        To limit this, pass a .txt file with the list of filenames relative to data/dir to sample from. --random_selections x y z (Where z is the optional text file)')
    parser.add_argument('--avoid_annotations', default=None, type=str, help="Path to .csv file with annotations of upcalls to avoid. Only used with --random_selections. If the annotations option is being used, this argument is ignored.")
    parser.add_argument('--seed', default=None, type=int, help='Seed for random number generator')
    parser.add_argument('--output', default=None, type=str, help='HDF5 dabase name. For isntance: db.h5')
    parser.add_argument('--overwrite', default=False, type=boolean_string, help='Overwrite the database. Otherwise append to it')
    parser.add_argument('--custom_module', default=None, type=str, help='Path to the folder containing custom components, such as a custom audio representation.')
    parser.add_argument('--only_augmented', default=False, type=boolean_string, help='Only include time-shifted instances without original annotations')
    args = parser.parse_args()

    create_db(
        data_dir=args.data_dir,
        audio_representation=args.audio_representation,
        annotations=args.annotations,
        annotation_step=args.annotation_step,
        step_min_overlap=args.step_min_overlap,
        labels=args.labels,
        output=args.output,
        table_name=args.table_name,
        random_selections=args.random_selections,
        avoid_annotations=args.avoid_annotations,
        overwrite=args.overwrite,
        seed=args.seed,
        custom_module=args.custom_module,
        only_augmented=args.only_augmented
    )

if __name__ == "__main__":
    main()