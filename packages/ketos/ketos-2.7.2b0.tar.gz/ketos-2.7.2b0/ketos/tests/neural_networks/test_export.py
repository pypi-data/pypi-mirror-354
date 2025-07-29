# ================================================================================ #
#   Authors: Fabio Frazao and Oliver Kirsebom                                      #
#   Contact: fsfrazao@dal.ca, oliver.kirsebom@dal.ca                               #
#   Organization: MERIDIAN (https://meridian.cs.dal.ca/)                           #
#   Team: Data Analytics                                                           #
#   Project: ketos                                                                 #
#   Project goal: The ketos library provides functionalities for handling          #
#   and processing acoustic data and applying deep neural networks to sound        #
#   detection and classification tasks.                                            #
#                                                                                  #
#   License: GNU GPLv3                                                             #
#                                                                                  #
#       This program is free software: you can redistribute it and/or modify       #
#       it under the terms of the GNU General Public License as published by       #
#       the Free Software Foundation, either version 3 of the License, or          #
#       (at your option) any later version.                                        #
#                                                                                  #
#       This program is distributed in the hope that it will be useful,            #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#       GNU General Public License for more details.                               # 
#                                                                                  #
#       You should have received a copy of the GNU General Public License          #
#       along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
# ================================================================================ #

""" Unit tests for the 'neural_networks.dev_utils.export' module within the ketos library
"""
import pytest
import os
import numpy as np
import shutil
from zipfile import ZipFile
from pathlib import Path
from ketos.neural_networks import load_model_file
from ketos.audio import load_audio_representation_from_file
from ketos.data_handling.parsing import load_audio_representation
import ketos.neural_networks.dev_utils.export as exp

current_dir = Path(__file__).parent
path_to_assets = (current_dir / '..' / 'assets').resolve() # resolve converts the path to an absolute path
# path_to_tmp = path_to_assets / 'tmp'

def test_export_to_ketos_protobuf(tmpdir):
    """Test export resnet to ketos-protobuf format"""
    # model, audio_repr = load_model_file(model_path, tmp_path, load_audio_repr=True)
    model_path = path_to_assets / 'narw_resnet.kt'
    model = load_model_file(model_path)
    audio_repr = load_audio_representation_from_file(model_path)[0]['spectrogram']
    output_path = tmpdir / 'narw1.ktpb'

    exp.export_to_ketos_protobuf(model=model, output_name=output_path, audio_repr=audio_repr, 
        input_shape=(94,129), backward_compat=False)
    
    #check that file exists:
    assert (output_path).is_file()
    
    # check that file has correct content:
    with ZipFile(output_path, 'r') as zip:
        zip.extractall(path=tmpdir)
    
    assert (tmpdir / 'model').is_dir()
    assert (tmpdir / 'recipe.json').is_file()
    assert (tmpdir / 'audio_repr.json').is_file()

    # load audio representation
    audio_repr = load_audio_representation((tmpdir / 'audio_repr.json'), return_unparsed=True)
    assert 'spectrogram' in audio_repr

    # check that duration was written to file
    a = audio_repr['spectrogram']
    assert 'duration' in a
    assert a['duration'] == "3.008 s"

    # check that input_shape was written to file
    assert 'input_shape' in a
    assert a['input_shape'] == [1,94,129,1]

    # shutil.rmtree(tmp_path) #clean up


def test_export_to_ketos_protobuf_backward_compat(tmpdir):
    """Test export resnet to ketos-protobuf format backward compatible"""
    model_path = (path_to_assets / 'narw_resnet.kt')
    model, audio_repr = load_model_file(model_path, tmpdir, load_audio_repr=True)
    output_path = (tmpdir / 'narw1.ktpb')

    exp.export_to_ketos_protobuf(model=model, output_name=output_path, audio_repr=audio_repr[0], 
        input_shape=(1,94,129,1))
    
    assert (output_path).is_file()


def test_export_to_ketos_protobuf_infer_shape(tmpdir):
    """Test export resnet to ketos-protobuf format can infer shape"""
    model_path = path_to_assets / 'narw_resnet.kt'
    model, audio_repr = load_model_file(model_path, tmpdir, load_audio_repr=True)
    output_path = tmpdir / 'narw1.ktpb'

    with pytest.raises(AssertionError):
        exp.export_to_ketos_protobuf(model=model, output_name=output_path, audio_repr=audio_repr[0])

    exp.export_to_ketos_protobuf(model=model, output_name=output_path, audio_repr=audio_repr[0], duration=3.0)

    # check that file exists:
    assert (output_path).is_file()

    # check that shape was inferred correctly
    with ZipFile(output_path, 'r') as zip:
        zip.extractall(path=tmpdir)
    audio_repr = load_audio_representation(tmpdir / 'audio_repr.json')
    assert audio_repr['spectrogram']['input_shape'] == [1,94,129,1]


def test_export_to_ketos_protobuf_audio_repr(tmpdir):
    """Test export resnet to ketos-protobuf format using audio representation file path"""
    model_path = path_to_assets / 'narw_resnet.kt'
    audio_repr_path = path_to_assets / 'audio_repr.json'
    
    model = load_model_file(model_path, tmpdir)
    output_path = tmpdir / 'narw2.ktpb'

    exp.export_to_ketos_protobuf(model=model, output_name=output_path, audio_repr=audio_repr_path, 
        overwrite=True, duration=3.0)

    assert (output_path).is_file


def test_export_to_protobuf(tmpdir):
    """Test export resnet to protobuf format"""
    model_path = path_to_assets / 'narw_resnet.kt'
    model = load_model_file(model_path, tmpdir)
    input_spec = np.ones(shape=(94,129))
    model.run_on_instance(input_spec, input_transform_function=model._transform_input)
    output_path = tmpdir / 'model.pb'

    exp.export_to_protobuf(model=model, output_name=str(output_path))

    assert output_path.is_dir()


def test_export_to_ketos(tmpdir):
    """Test export resnet to ketos format"""
    model_path = path_to_assets / 'narw_resnet.kt'
    model = load_model_file(model_path)
    audio_repr = load_audio_representation_from_file(model_path)[0]['spectrogram']

    # check that we can save model
    output_path = tmpdir / 'narw3.kt'
    exp.export_to_ketos(model=model, output_name=output_path)
    assert os.path.isfile(output_path)

    # check that we can save specific checkpoint
    output_path = tmpdir / 'narw4.kt'
    exp.export_to_ketos(model=model, output_name=output_path, checkpoint_name="cp-0030.ckpt")
    assert os.path.isfile(output_path)

    # check that audio representation is saved correctly
    output_path = tmpdir / 'narw5.kt'
    exp.export_to_ketos(model=model, output_name=output_path, audio_repr=audio_repr)
    assert os.path.isfile(output_path)

    with ZipFile(output_path, 'r') as zip:
        zip.extractall(path=tmpdir)
    audio_repr = load_audio_representation(tmpdir / 'audio_repr.json')
    assert audio_repr['window'] == 0.256

    # check that we can save extra files to the .kt archive
    output_path = tmpdir / 'narw6.kt'
    exp.export_to_ketos(model=model, output_name=output_path, extra=(path_to_assets / "annot_001.csv"))
    assert os.path.isfile(output_path)

    with ZipFile(output_path, 'r') as zip:
        zip.extractall(path=tmpdir)
    assert (tmpdir / "annot_001.csv").exists()
    

def test_ketos_save_custom_module(tmpdir):
    """ Check if custom files are save correctly to the custom folder
        when using the custom_module parameter
    """
    model_path = (path_to_assets / 'narw_resnet.kt')
    model = load_model_file(model_path)

    custom_module = tmpdir / 'custom_module'
    os.mkdir(custom_module)
    (custom_module / 'another_file.py').touch()
    (custom_module / 'nn_architecture.py').touch()

    output_path = tmpdir / 'narw.kt'
    exp.export_to_ketos(model=model, output_name=output_path, custom_module=custom_module)
    with ZipFile(output_path, 'r') as archive:
        assert 'custom/nn_architecture.py' in archive.namelist()
        assert 'custom/another_file.py' in archive.namelist()

def test_get_export_function():
    """Test that we can detect the appropriate export function"""
    assert exp.get_export_function('/test/out.pb') == exp.export_to_protobuf
    assert exp.get_export_function('/test/out.kt') == exp.export_to_ketos
    assert exp.get_export_function('/test/out.ktpb') == exp.export_to_ketos_protobuf
    assert exp.get_export_function('/test/out.aaa') == exp.export_to_ketos
