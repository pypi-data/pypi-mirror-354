from ketos.neural_networks.cnn import CNNInterface, CNN1DInterface
from ketos.neural_networks.resnet import ResNetInterface, ResNet1DInterface
from ketos.neural_networks.densenet import DenseNetInterface
from ketos.neural_networks.inception import InceptionInterface
from zipfile import ZipFile
from pathlib import Path
from ketos.utils import load_module
import warnings
import importlib
import sys
import zipimport
import json


interface_names_in_recipes = {'CNNInterface':CNNInterface,
                              'CNN1DInterface':CNN1DInterface,
                              'ResNetInterface':ResNetInterface,
                              'ResNet1DInterface':ResNet1DInterface,
                              'DenseNetInterface':DenseNetInterface,
                              'InceptionInterface':InceptionInterface}

def load_model_file(model_file, new_model_folder='kt-tmp', overwrite=True, load_audio_repr=False, replace_top=False, diff_n_classes=None):
    """ Load a model from a ketos (.kt) model file.
        
        Args:
            model_file:str
                Path to the ketos(.kt) file
            new_model_folder:str
                Path to folder where files associated with the model will be stored.
                By default the files will be saved to a folder named 'kt-tmp' created 
                in the current working directory.
            overwrite: bool
                If True, the 'new_model_folder' will be overwritten.
            replace_top: bool
                If True, the classification top of the model will be replaced by a new, untrained one.
                What is actually replaced (i.e.: what exactly is the "top") is defined by the architecture.
                It is usually a block of dense layers with the appropriate activations. Default is False.
            diff_n_classes: int
                Only relevant when 'replace_top' is True.
                If the new model should have a different number of classes it can be specified by this parameter.
                If left to none, the new model will have the same number of classes as the original.
            load_audio_repr: bool
                If True, look for an audio representation included with the model. 
                
        Raises:
            ValueError: If the model recipe does not contain a valid value for the 'interface' field.

        Returns:
            model_instance: The loaded model
            audio_repr: If load_audio_repr is True, also return a dictionary with the loaded audio representation.

    """
    # First we need to get the recipe file to know which Interface we are working with.
    path = Path(model_file).resolve()
    with ZipFile(path, 'r') as archive: # we dont need to extract from the zipfile, we can just load directly into memory
        recipe_file = archive.open('recipe.json')
        nn_recipe = json.load(recipe_file)
    
    # The script prioritizes custom architectrues over the default ones from ketos. So if the user defined a custom architecture with the same name as a default one, it will prioritize the custom
    # if there is no custom_architecture it will attempt to load a default one
    try:
        # See docs https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
        module_name = "nn_architecture" #The file name will always be custom_architecture because this is how ketos saves it
        module_path = zipimport.zipimporter(path / "custom") # the folder name within the zip archive will always be custom
        spec = module_path.find_spec(module_name)

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module # adding the module to the list of modules in sys
        spec.loader.exec_module(module) # actually load the module, this is equivalent to importing
        # Now we load the class
        interface = getattr(module, nn_recipe['interface'])
        # Warn the user about using a custom input transform function
        warnings.warn("Ketos detected a custom nn architecture and will be using that.", UserWarning)
    except AttributeError:
        # fallback to the dictionary
        try:
            # load the class from the default interfaces in ketos
            interface = interface_names_in_recipes[nn_recipe['interface']]
        except KeyError as e:
            e.__suppress_context__ = True # we are supressing the first attribute error as it is not useful
            raise ValueError("The model recipe does not indicate a valid interface")
    

    # load the model with the appropriate interface
    loaded = interface.load(model_file=model_file, new_model_folder=new_model_folder, overwrite=overwrite, load_audio_repr=load_audio_repr,  replace_top=replace_top, diff_n_classes=diff_n_classes)
    return loaded

def import_nn_interface(name, module_path=None):
    ''' Import neural network interface class

        Args:
            name: str
                Name of the interface class, e.g., 'DenseNetInterface'. Can be either a standard ketos interface or a custom class.
            module_path: str
                Path to the Python module file, e.g., 'nn/densenet.py'. Only required if the 
                interface is not a standard ketos interface. Defaults to None.
            
        Returns:
            : class derived from ketos.neural_networks.nn_interface.NNInterface
    '''
    try:
        if module_path:
            path = Path(module_path).resolve()
            module = load_module(path, module_name=None)
            interface = getattr(module, name, None)
            
            if interface is None:
                raise AttributeError(f"{interface} function not found in the module.")
            print("Ketos detected a custom nn architecture and will be using that.")
        else:
            raise AttributeError  # Explicitly trigger the except block for standard interfaces
    except AttributeError:
        try:
            # load the class from the default interfaces in ketos
            interface = interface_names_in_recipes[name]
        except KeyError as e:
            e.__suppress_context__ = True # we are supressing the first attribute error as it is not useful
            raise ValueError("The model recipe does not indicate a valid interface")

    return interface

def load_input_transform_function(source, function_name="transform"):
    """ Load a input transform function from a ketos (.kt) model file or directory.
        
        Args:
            source: str
                Path to the ketos(.kt) file or directory
            function_name: str
                Name of the transfrom function

        Returns:
            function: The input transform function

    """
    # loads a custom input transform function from the model file.
    # Gives an Attribute error if there is none

    path = Path(source).resolve()
    module_name = "input_transform_function" #The file name will always be custom_architecture because this is how ketos saves it
    module = load_module(path, module_name=None)    
    function = getattr(module, function_name, None)
    
    if function is None:
        raise AttributeError(f"{function_name} function not found in the module.")
    
    return function

def load_export_transform_function(model_file, function_name="transform"):
    """ Load an export transform function from a ketos (.kt) model file.
        
        Args:
            model_file:str
                Path to the ketos(.kt) file

        Returns:
            function: The export transform function

    """
    # loads a custom input transform function frrom the model file if there is one
    # Otherwise giver error

    path = Path(model_file).resolve()

    module_name = "output_transform_function" #The file name will always be custom_architecture because this is how ketos saves it
    module_path = zipimport.zipimporter(path / "custom") # the folder name within the zip archive will always be custom
    spec = module_path.find_spec(module_name)

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module # adding the module to the list of modules in sys
    spec.loader.exec_module(module) # actually load the module, this is equivalent to importing
    # Now we load the function
    function = getattr(module, function_name)

    return function
