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

""" Unit tests for the 'parsing' module within the ketos library
"""
import json
import ketos.data_handling.parsing as jp

def test_parse_audio_representation(spectr_settings):
    from ketos.audio.spectrogram import MagSpectrogram
    data = json.loads(spectr_settings)
    data['spectrogram']['dummy'] = 'hest'
    d = jp.parse_audio_representation(data['spectrogram'])
    assert d['rate'] == 20000
    assert d['window'] == 0.1
    assert d['step'] == 0.025
    assert d['window_func'] == 'hamming'
    assert d['freq_min'] == 30
    assert d['freq_max'] == 3000
    assert d['duration'] == 1.0
    assert d['resample_method'] == 'scipy'
    assert d['type'] == MagSpectrogram
    assert not d['normalize_wav']
    assert d['transforms'] == [{"name":"enhance_signal", "enhancement":1.0}, {"name":"adjust_range", "range":(0,1)}]
    assert d['waveform_transforms'] == [{"name":"add_gaussian_noise", "sigma":0.2}]
    assert d['decibel']
    assert d['dummy'] == 'hest'

def test_parse_audio_with_custom_representation(custom_audio_representation_module, spectr_settings):
    data = json.loads(spectr_settings)
    data['spectrogram']['type'] = 'CustomRepresentation'
    data['spectrogram']['dummy'] = 'hest'

    parsed_data = jp.parse_audio_representation(data['spectrogram'], custom_audio_representation_module)
    
    assert parsed_data['rate'] == 20000
    assert parsed_data['window'] == 0.1
    assert parsed_data['step'] == 0.025
    assert parsed_data['window_func'] == 'hamming'
    assert parsed_data['freq_min'] == 30
    assert parsed_data['freq_max'] == 3000
    assert parsed_data['duration'] == 1.0
    assert parsed_data['resample_method'] == 'scipy'
    assert not parsed_data['normalize_wav']
    assert parsed_data['transforms'] == [{"name": "enhance_signal", "enhancement": 1.0}, {"name": "adjust_range", "range": (0, 1)}]
    assert parsed_data['waveform_transforms'] == [{"name": "add_gaussian_noise", "sigma": 0.2}]
    assert parsed_data['decibel']
    assert parsed_data['dummy'] == 'hest'

    custom_class = parsed_data['type']
    custom_instance = custom_class()
    assert custom_instance.window == '0.2'

def test_parse_parameter():
    assert jp.parse_parameter(name='window', value='7.3 ms') == 0.0073
    assert jp.parse_parameter(name='window2', value='7.3 ms') == '7.3 ms'

def test_encode_parameter():
    assert jp.encode_parameter(name='window', value=8.2) == '8.2 s'
    assert jp.encode_parameter(name='window2', value=8.2) == 8.2
    assert jp.encode_parameter(name='window3', value=[8.2]) == [8.2]
    assert jp.encode_parameter(name='dummy', value=(8.2, 4, 66)) == "(8.2,4,66)"

def test_encode_audio_representation():
    s = {'type': 'bla', 'window': 0.032, 'dummy': ['x', 'y'], 'transforms':[]}
    s = jp.encode_audio_representation(s)
    assert s['window'] == '0.032 s'
    assert s['dummy'] == ['x', 'y']
    assert s['transforms'] == []
    s = {'myrep': {'type': 'bla', 'window': 0.032, 'dummy': ['x', 'y'], 'transforms':[]}}
    s = jp.encode_audio_representation(s)
    assert s['myrep']['window'] == '0.032 s'
    assert s['myrep']['dummy'] == ['x', 'y']
    assert s['myrep']['transforms'] == []

def test_is_encoded():
    s = {'type': 'bla', 'window': 0.032, 'dummy': 'xx'}
    assert not jp.is_encoded(s)
    s = {'type': 'bla', 'window': '0.032s', 'dummy': 'xx'}
    assert jp.is_encoded(s)
    s = {'type': 'bla', 'step':0.32, 'window': '0.032s', 'dummy': 'xx'}
    assert not jp.is_encoded(s)
    s = {'myrepr': {'type': 'bla', 'step':0.32, 'window': '0.032s', 'dummy': 'xx'}}
    assert not jp.is_encoded(s)
    s = {'myrepr': {'type': 'bla', 'step':"0.32s"}}
    assert jp.is_encoded(s)
