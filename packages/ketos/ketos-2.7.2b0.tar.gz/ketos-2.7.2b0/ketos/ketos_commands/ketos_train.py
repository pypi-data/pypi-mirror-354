import numpy as np
import warnings
import yaml
import json
import tables
from typing import Callable
from pathlib import Path
from ketos.data_handling.data_feeding import BatchGenerator, JointBatchGen
from ketos.ketos_commands.ketos_logger import KetosLogger
from ketos.ketos_commands.constants import EXIT_ERROR, EXIT_INTERRUPTION, EXIT_SUCCESS

def load_config(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        try:
            return json.loads(content)  # Try JSON first
        except json.JSONDecodeError:
            return yaml.safe_load(content)  # Then try YAML


def train_model(
        model: str, 
        hdf5_db: str, 
        audio_representation: str = None, 
        train_table: str | list[str] = '/', 
        train_annot_table: str | list[str] = None, 
        val_table: str | list[str] = None, 
        val_annot_table: str | list[str] = None, 
        x_field: str = None,
        batch_size: int | list[int] = 32, 
        epochs: int = 20, 
        overwrite: bool = True,
        seed: int = None,
        output_folder: str = None, 
        model_output: str = None, 
        checkpoints: int = None, 
        custom_module: str = None,
        log_file: str = 'ketos-train.log',
        replace_head: int = None,
        freeze_features: bool = False,
    ) -> None:
    """
    Train or fine-tune a neural network model using data stored in an HDF5 database.

    This function supports both training from scratch (via a model recipe) and fine-tuning an existing model (.kt file). 
    It also allows integration of user-defined custom components for transformation and architecture.

    Custom files that can be created if using custom_module (the files must be named accordingly and stored in the same folder):
        nn_architecture.py: Defines custom neural network architectures.
        input_transform_function.py: A function named 'transform' to manipulate data and labels before they are fed to the network.
        audio_representation.py: Script for processing raw audio into the desired format. Only used for ketos-run.
        output_transform_function.py: A function named 'transform' to manipulate the network output. Not used during training but required for inference when using ketos-run if a non-default behaviour is desired.

    Args:
        model: Path to the model recipe (.json or .yaml) or to a pre-trained model file (.kt). 
                If a recipe is provided, training starts from scratch. If a .kt file is provided, the model will be fine-tuned.
        hdf5_db: Path to the HDF5 database file containing training and validation data.
        audio_representation: Path to the audio representation config file (YAML/JSON). Required only when training from a recipe. 
                              This file is stored as model metadata for future reference.
        train_table: Path(s) within the HDF5 database where the training data is stored. Defaults to None.
        train_annot_table: Path(s) within the HDF5 database where the training annotations (labels) are stored as a separate table, 
                    in case they are not included as fields in train_table. 
                    Defaults to None.
        val_table: Path(s) within the HDF5 database where the validation data is stored. Defaults to None.
        val_annot_table: Path(s) within the HDF5 database where the validation annotations (labels) are stored as a separate table, 
                    in case they are not included as fields in val_table.
                    Defaults to None.
        x_field: Field name in the HDF5 tables representing the input data (e.g., "data", "spectrogram", "mel_spec").
        batch_size: Batch size for training. Can be an integer or a list of integers for custom batch sizes.
                    If a single integer is passed, it will be distributed evenly across the tables. For example, a batch size of 32 with two tables (/train/pos and /train/neg) will allocate 16 for one and 16 for the other.
                    If a list of integers is passed, the length of the list must match the number of tables. For example, if there are two tables and the batch size is specified as --batch_size 32 64, the first table will have a batch size of 32 and the second will have a batch size of 64.
                    Defaults to 32.
        epochs: Number of training epochs. Defaults to 20.
        overwrite: Boolean flag indicating whether to overwrite existing checkpoints or resume training. 
               If True, the model will be trained from scratch and any existing checkpoints will be overwritten. 
               If False, the training process will attempt to resume from existing checkpoints, if available.
               Defaults to True.
        seed: Seed for random number generator for reproducibility. Defaults to None.
        output_folder: Directory to save model outputs. Defaults to None.
        model_output: Filename to save the trained model. Defaults to None.
        checkpoints: Frequency (in epochs) to save checkpoints during training. Defaults to None.
        custom_module: Directory containing custom components like neural network architectures and transformation functions. Defaults to None.
        log_file: Name of the log file. Defaults to "ketos-train.log. Not to be confused the log .csv files reporting the training metrics.".
        replace_head: If specified (as an int), replaces the classification layer with a new one having this many output classes. Only applicable when fine-tuning a pretrained model (.kt).
        freeze_features: If True, freezes the feature extractor layers during training. Useful when fine-tuning with a small dataset or replacing the classification head.

    Note:
        The train_table and val_table parameters accept either a single path or a list of paths. Specifying a root path (e.g., '/train') will include all subpaths under it. If multiple paths are specified, only those exact paths are used for data retrieval.
        Separate annotation tables (train_annot_table and val_annot_table) must match the data tables (train_table and val_table) in order if specified. If omitted, labels are assumed to be part of the data tables.
    Returns:
        None
    """
    # These more heavy imports are here so that we don`t show lots of initialization messages upon doing just a simple --help
    import tensorflow as tf
    from ketos.neural_networks import import_nn_interface, load_model_file, load_input_transform_function
        
    if seed is not None:
        np.random.seed(seed) #set random seeds
        tf.random.set_seed(seed)

    model_path = Path(model)
    is_pretrained = model_path.suffix == '.kt'
    
    if custom_module:
        custom_module = Path(custom_module)

    nn_interface_module_path = custom_module / "nn_architecture.py" if custom_module else None
    
    if is_pretrained: # it is a .kt file
        try:
            # load the model from the .kt file
            model = load_model_file(
                str(model_path),
                replace_top=replace_head is not None,
                diff_n_classes=replace_head,
                load_audio_repr=False
            )
        except AttributeError as e:
            raise AttributeError("Model does not support classification layer replacement.") from e
    else: # It is a recipe
        nn_recipe = load_config(str(model_path))
        nn_interface = import_nn_interface(name=nn_recipe['interface'], module_path=str(nn_interface_module_path) if nn_interface_module_path else None)
        model = nn_interface.build(str(model_path))


    # Freeze the feature extraction layers, This is not very flexible, But it works for the moment.
    if freeze_features:
        for layer in model.model.layers[:-2]:
            layer.trainable = False
    
    if not is_pretrained:
        if audio_representation is None:
            raise ValueError("Audio representation config file is required when training from a recipe.")
        audio_repr_config = load_config(audio_representation)
        if x_field is None:
            if isinstance(audio_repr_config, dict):
                # Extract the top-level key as the default x_field
                x_field = next(iter(audio_repr_config.keys()))
            else:
                raise ValueError("Failed to infer x_field from the audio configuration. Provide it explicitly.")

    # Attempting to load a input trainsform functor first from a custom module if it exists; from the nn_interface otherwiser; None if neither is found
    if custom_module and (custom_module / 'input_transform_function.py').exists():
        input_transform_func = load_input_transform_function(custom_module / 'input_transform_function.py')
        print("Custom input_transform_function detected and loaded from user-provided module.")
        input_transform_func = input_transform_func
    elif is_pretrained and hasattr(model, 'transform_batch'):
        input_transform_func = model.transform_batch
    elif not is_pretrained and hasattr(nn_interface, 'transform_batch'):
        input_transform_func = nn_interface.transform_batch
    else:
        warnings.warn("Failed to load an input_transform_function, attempting to continue without one.", UserWarning)
        input_transform_func = None

    y_field = getattr(input_transform_func, 'y_field', 'label')

    # Open the database
    db = tables.open_file(hdf5_db, 'r')
    train_gens = _create_batch_generators(train_table, batch_size, db, x_field=x_field, input_transform_func=input_transform_func, is_training=True, annot_table=train_annot_table, y_field=y_field)
    train_generator = JointBatchGen(train_gens, n_batches="min", shuffle_batch=False, reset_generators=False) # join generators

    if val_table is not None:
        val_gens = _create_batch_generators(val_table, batch_size, db, x_field=x_field, input_transform_func= input_transform_func, is_training=False, annot_table=val_annot_table, y_field=y_field)
        val_generator = JointBatchGen(val_gens, n_batches="min", shuffle_batch=False, reset_generators=False)

    output_folder = Path(output_folder or '.').resolve()
    output_folder.mkdir(parents=True, exist_ok=True)
    checkpoint_dir = output_folder / 'checkpoints'

    if not overwrite and checkpoint_dir.exists():
        latest_checkpoint = tf.train.latest_checkpoint(checkpoint_dir) # Try to load checkpoints and resume from the latest checkpoint
        if latest_checkpoint:
            latest_checkpoint = Path(latest_checkpoint)
            # Extract epoch number from the checkpoint name, assuming format cp-XXXX.ckpt.index
            start_epoch = int(latest_checkpoint.name.split('-')[1].split('.')[0]) # is there a better way to extract just the number?
            model.model.load_weights(latest_checkpoint).expect_partial()
            if start_epoch >= epochs:
                print("Training is already complete. No further epochs to run.")
                db.close()
                return  # Exit early if training is already done
                
            print(f"Resuming from checkpoint: {latest_checkpoint} (starting at epoch {start_epoch+1})")
            log_mode = "a"
        else:
            log_mode = "w"
            start_epoch = 0
            # If no checkpoints found, raise a warning and proceed to train from scratch
            warnings.warn(f"Could not find checkpoints in {str(checkpoint_dir)}. Starting training from scratch.", category=UserWarning)
    else:
        log_mode = "w"
        start_epoch = 0
    
    # set generators
    model.train_generator = train_generator
    if val_table is not None:
        model.val_generator = val_generator
    
    model.log_dir = str(output_folder)
    model.checkpoint_dir = str(checkpoint_dir) 

    if model_output is None:
        model_output = "ketos_trained_model.kt"

    model_output_path = output_folder / model_output
    # Check if name already has extension otherwise add it
    if model_output_path.suffix != '.kt':
        model_output_path = model_output_path.with_suffix('.kt')
    
    if checkpoints is None:
        checkpoints = epochs

    logger = KetosLogger('ketos-train', str(Path(output_folder, log_file)), mode=log_mode, format='yaml')
    log_params = {}
    if not is_pretrained:
        log_params['model_recipe'] = str(model_path)
        log_params['audio_representation'] = audio_representation

    log_params.update({
        'hdf5_db': hdf5_db,
        'train_table': train_table,
        'train_annot_table': train_annot_table,
        'val_table': val_table,
        'val_annot_table': val_annot_table,
        'batch_size': batch_size,
        'epochs': epochs,
        'overwrite': overwrite,
        'seed': seed,
        'output_folder': str(output_folder),
        'model_output': model_output,
        'checkpoints': checkpoints,
        'custom_module': custom_module,
        'log_file': log_file,
        'replace_head': replace_head,
        'freeze_features': freeze_features
    })
    
    logger.info("Resuming training" if log_mode == 'a' else "Training started",
            stdout=False,
            **{'parameters': log_params, 'status': 'success'})

    # train the network
    print("\nTraining Starting ...")
    try:
        model.train_loop(n_epochs=epochs, verbose=True, log_csv=True, 
                         csv_name="log_" + model_output_path.stem + ".csv", 
                         validate=(val_table is not None), start_epoch=start_epoch, checkpoint_freq=checkpoints)
    except KeyboardInterrupt as e:
        logger.error('Process was interrupted by user.', stdout=False, **{
            'status': 'interruption'
        })
        raise
    except Exception as e:
        logger.error(f'{e}', stdout=True, **{'status': 'error'})
        raise

    try:
        print(f"Saving model to {model_output_path}")
        model.save(output_name=str(model_output_path), audio_repr=audio_representation, custom_module=custom_module)
        logger.info(f"Process finished. Output saved to: {output_folder}", stdout=False, **{
            'output': {
                'folder': str(output_folder)
            },
            'status': 'success'
        })
    except Exception as e:
        logger.error(f'{e}', stdout=True, **{'status': 'error'})
        raise

    db.close()

def _create_batch_generators(
        table: str | list[str], 
        batch_size: int | list[int], 
        db: tables.file, 
        x_field: str,
        input_transform_func: Callable = None, 
        annot_table: str | list[str] = None, 
        is_training: bool = True, 
        y_field: str | list[str] = 'label'
    ) -> list[BatchGenerator]:
    """
    Create batch generators for data retrieval from a specified database table.
    
    This function supports dynamic batch generation for training or validation purposes,
    facilitating the handling of balanced or imbalanced datasets by adjusting batch sizes
    per class or subgroup.

    Args:
        table: The path(s) to the database table(s) containing the data.
        batch_size: The size of batches to generate. If a list, it should match the number of tables.
        db: Database connection object or identifier.
        x_field: Field name specifying the input data.
        input_transform_func: A function to apply to input data during batch generation.
        annot_table: Table(s) containing annotations. Defaults to None.
        is_training: Flag to indicate whether the generator is used for training (affects data shuffling and refresh).
        y_field: Field name(s) specifying the output labels. Defaults to 'label'.
        

    Returns:
        A list of BatchGenerator instances configured per the specified parameters.
    
    Raises:
        ValueError: If the length of `batch_size` does not match the number of tables or leaf nodes.
    """
    table_type_str = 'train' if is_training else 'val'
    # This code will create a generator for each subgroup within a table. This will ensure that each batch will contain the same number of samples for each class
    # For intance if the table has /train/positives and /train/negatives, the code will create 2 generators, with batch size = batch_size/2 for each label and join them later
    gens = []
    # Handling if the table is a list of paths (multiple tables)
    if isinstance(table, list):
        # Calculate the appropriate batch sizes for each subgroup
        if isinstance(batch_size, list):
            if len(batch_size) != len(table):
                raise ValueError(f"The length of batch_size must match the length of {table_type_str}_table.")
            batch_sizes = batch_size
        else:
            batch_sizes = [int(batch_size / len(table))] * len(table) # Distribute data evenly

        if annot_table is None:
            annot_table = [None] * len(table)
        elif len(annot_table) < len(table):
            # completing the remaining annot_table with None. This will result in only the first portion of the data tables to have a corresponding annot table.
            # Useful if for instance background data is implicitly of a certain class.
            annot_table.extend([None] * (len(table) - len(annot_table))) 
            
        for path, batch_size, annot in zip(table, batch_sizes, annot_table): 
            group = db.get_node(path)
            if not isinstance(group, tables.Leaf):
                group = db.get_node(path + '/data')

            annot_node = db.get_node(annot) if annot is not None else None

            generator = BatchGenerator(batch_size=batch_size,
                                       data_table=group,
                                       annot_table=annot_node,
                                       output_transform_func=input_transform_func,
                                       shuffle=True, 
                                       select_indices=None,
                                       refresh_on_epoch_end=is_training, 
                                       x_field=x_field,
                                       y_field=y_field)
            gens.append(generator)
    # Handling if the table is a single string (one group which could have multiple subtables as leaf nodes)
    elif isinstance(table, str):
        root_node = db.get_node(table)
        if isinstance(root_node, tables.Leaf):
            leaf_nodes = [root_node]
        else:
            leaf_nodes = [group for group in db.walk_nodes(table, "Table")]

        # Calculate the appropriate batch sizes for each subgroup
        if isinstance(batch_size, list):
            if len(batch_size) != len(leaf_nodes):
                raise ValueError(f"The length of batch_size must match the number of leaf nodes in {table_type_str}_table.")
            batch_sizes = batch_size
        else:
            batch_sizes = [int(batch_size / len(leaf_nodes))] * len(leaf_nodes)

        if isinstance(annot_table, list):
            annot_table = annot_table[0]

        # Create generators for each node
        for group, batch_size in zip(leaf_nodes, batch_sizes):
            annot_node = db.get_node(annot_table) if annot_table is not None else None
            generator = BatchGenerator(batch_size=batch_size,
                                       data_table=group,
                                       annot_table=annot_node,
                                       output_transform_func=input_transform_func,
                                       shuffle=True, 
                                       select_indices=None,
                                       refresh_on_epoch_end=is_training, 
                                       x_field=x_field,
                                       y_field=y_field)
            gens.append(generator)
    else:
        raise ValueError(f"{table_type_str} must be either a list of table paths or a string representing the table name.")

    return gens

def main():
    import argparse

    def boolean_string(s):
        if s not in {'False', 'True'}:
            raise ValueError('Not a valid boolean string')
        return s == 'True'

    # parse command-line args
    parser = argparse.ArgumentParser(description="Train or fine-tune a model using HDF5 datasets and Ketos interface.")
    
    parser.add_argument('model', type=str, help='Path to the model recipe (.json/.yaml) or a pre-trained model (.kt).')
    parser.add_argument('hdf5_db', type=str, help='Path to the HDF5 database file containing training and validation data')
    parser.add_argument('--audio_representation', default=None, type=str, help='Path to the audio representation config (only used when training from scratch). This file will be saved as metadata with the model. Only used when using a model recipe.')
    
    # Optional parameters for train and validation data paths
    parser.add_argument('--train_table', default='/', nargs='+', type=str, help='''Path(s) within the HDF5 database where the training data is stored. Can be a string or a list of strings specifying multiple paths.
    If a single path is passed, ketos-train will search for all leaf nodes under that root path and use all the data for training. For example, in an HDF5 database with paths /train/pos and /train/neg, specifying --train_table /train will use the data in both /train/pos and /train/neg.
    If multiple paths are passed, ketos-train will use only the data in those specified paths for training. For example, specifying --train_table /train/pos /train/neg will use only the data in /train/pos and /train/neg.
    ''')
    parser.add_argument('--train_annot_table', default=None, nargs='+', type=str, help='''Path(s) within the HDF5 database where the training annotations (labels) are stored as a separate table, 
                    in case they are not included as fields in train_table. Defaults to None.''')
    parser.add_argument('--val_table', default=None, nargs='+', type=str, help='''Path(s) within the HDF5 database where the training data is stored. Can be a string or a list of strings specifying multiple paths.
    If a single path is passed, ketos-train will search for all leaf nodes under that root path and use all the data for validation. For example, in an HDF5 database with paths /val/pos and /val/neg, specifying --val_table /val will use the data in both /val/pos and /val/neg.
    If multiple paths are passed, ketos-train will use only the data in those specified paths for training. For example, specifying --val_table /val/pos /val/neg will use only the data in /val/pos and /val/neg.
    ''')
    parser.add_argument('--val_annot_table', default=None, nargs='+', type=str, help='''Path(s) within the HDF5 database where the validation annotations (labels) are stored as a separate table, 
                    in case they are not included as fields in val_table. Defaults to None.''')
    parser.add_argument('--x_field', default=None, type=str, help='Field name in the HDF5 tables representing the' \
    ' input data (e.g., "data", "spectrogram", "mel_spec"). Overrides automatic detection from the audio representation config.')

    # Additional parameters
    parser.add_argument('--batch_size', default=32, type=int, nargs='+', help='''Batch size for training. Can be an integer or a list of integers for custom batch sizes.
    If a single integer is passed, it will be distributed evenly across the tables. For example, a batch size of 32 with two tables (/train/pos and /train/neg) will allocate 16 for one and 16 for the other.
    If a list of integers is passed, the length of the list must match the number of tables. For example, if there are two tables and the batch size is specified as --batch_size 32 64, the first table will have a batch size of 32 and the second will have a batch size of 64.''')
    parser.add_argument('--epochs', default=20, type=int, help='Number of training epochs.')
    
    # Overwrite parameter to control checkpoint resuming
    parser.add_argument('--overwrite', default=True, type=boolean_string, help='When set to False, the model will attempt to resume from existing checkpoints in the output folder, if any exist. If True, any existing checkpoints will be overwritten, starting a fresh training run. Default is True.')
    
    parser.add_argument('--seed', default=None, type=int, help='Seed for random number generator for reproducibility. Optional.')
    parser.add_argument('--output_folder', default=None, type=str, help='Directory to save model outputs.')
    parser.add_argument('--model_output', default=None, type=str, help='Filename to save the trained model. Optional.')
    parser.add_argument('--checkpoints', default=None, type=int, help='Frequency (in epochs) to save checkpoints during training. Optional.')
    parser.add_argument('--custom_module', default=None, type=str, help='Path to the folder containing custom components such as audio representation, neural network architecture, input transform function, and/or output transform function.')
    parser.add_argument('--log_file', default="ketos-train.log", type=str, help='Name of the log file to be created/used during the process. Defaults to "ketos-train.log". Not to be confused the log .csv files reporting the training metrics.')

    parser.add_argument('--replace_head', default=None, type=int, help='Replace classification layer with new head of specified output size.')
    parser.add_argument('--freeze_features', default=False, type=boolean_string, help='Whether to freeze feature extractor layers.')
    
    args = parser.parse_args()
    
    if isinstance(args.train_table, list) and len(args.train_table) == 1:
        args.train_table = args.train_table[0]
    if isinstance(args.val_table, list) and len(args.val_table) == 1:
        args.val_table = args.val_table[0]
    if isinstance(args.batch_size, list) and len(args.batch_size) == 1:
        args.batch_size = args.batch_size[0]

    train_model(**vars(args))

if __name__ == "__main__":
    main()