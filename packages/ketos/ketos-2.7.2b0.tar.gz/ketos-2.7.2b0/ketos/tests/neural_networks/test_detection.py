
import pytest
from unittest.mock import Mock, MagicMock
from ketos.neural_networks.dev_utils.detection import *
from ketos.audio.audio_loader import AudioFrameLoader
from ketos.ketos_commands.ketos_logger import KetosLogger
import numpy as np
import pandas as pd
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
path_to_assets = os.path.join(os.path.dirname(current_dir),"assets")
path_to_tmp = os.path.join(path_to_assets,'tmp')

@pytest.fixture
def batch():
    data = np.vstack([np.zeros((10,8,8)), np.ones((3,8,8)),np.zeros((10,8,8)), np.ones((3,8,8)),np.zeros((4,8,8))])
    support = np.array([('file_1.wav', i*0.5) for i in range(30)],dtype=[('filename', '|S10'), ('offset', '>f4')])
    return data, support



def test_compute_score_running_avg_basic():
    score = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    window_size = 3
    result = compute_score_running_avg(score, window_size)
    expected_result = np.array([1.33333333, 2., 3., 4., 5., 6., 7., 8., 9., 9.66666667])
    np.testing.assert_almost_equal(result, expected_result, decimal=7)

def test_compute_score_running_avg_empty_list():
    score = []
    window_size = 3
    with pytest.raises(ValueError):
        compute_score_running_avg(score, window_size)

def test_compute_score_running_avg_zero_window():
    score = [1, 2, 3, 4, 5]
    window_size = 0
    with pytest.raises(ValueError):
        compute_score_running_avg(score, window_size)

def test_compute_score_running_avg_even_window():
    score = [1, 2, 3, 4, 5]
    window_size = 2
    with pytest.raises(ValueError):
        compute_score_running_avg(score, window_size)

def test_compute_score_running_avg_large_window():
    score = [1, 2, 3, 4, 5]
    window_size = 7
    with pytest.raises(ValueError):
        compute_score_running_avg(score, window_size)

def test_compute_score_running_avg_non_integer_window():
    score = [1, 2, 3, 4, 5]
    window_size = 2.5
    with pytest.raises(TypeError):
        compute_score_running_avg(score, window_size)

def test_compute_score_running_avg_2d():
    score = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]])
    window_size = 3
    expected_output = np.array([[1.33333333, 1.33333333], [2., 2.], [3., 3.], [4., 4.], [4.66666667, 4.66666667]])
    assert np.allclose(compute_score_running_avg(score, window_size), expected_output)



def test_apply_detection_threshold_threshold_filtering():
    score = [0.2, 0.7, 0.3]
    threshold = 0.5
    expected_output = [(1, 0.7)]
    assert apply_detection_threshold(score, threshold) == expected_output

def test_apply_detection_threshold_multiple_valid_scores():
    score = [0.6, 0.4, 0.8]
    threshold = 0.5
    expected_output = [(0, 0.6), (2, 0.8)]
    assert apply_detection_threshold(score, threshold) == expected_output

def test_apply_detection_threshold_highest_score_only():
    score = [0.6, 0.4, 0.8]
    threshold = 0.6
    expected_output = [(2, 0.8)]
    assert apply_detection_threshold(score, threshold, True) == expected_output

def test_apply_detection_threshold_no_scores_above_threshold():
    score = [0.2, 0.3, 0.4]
    threshold = 0.5
    expected_output = []
    assert apply_detection_threshold(score, threshold) == expected_output

def test_apply_detection_threshold_empty_scores():
    score = []
    threshold = 0.5
    expected_output = []
    assert apply_detection_threshold(score, threshold) == expected_output

def test_test_apply_detection_threshold_empty_scores_scores_at_threshold():
    score = [0.2, 0.5, 0.3, 0.5, 0.8]
    threshold = 0.5
    expected_output = [(1, 0.5), (3, 0.5), (4, 0.8)]
    assert apply_detection_threshold(score, threshold) == expected_output




def test_filter_by_threshold_filter_with_scores_above_threshold():
    detections = {
        'filename': ['file1', 'file2'],
        'start': [0, 1],
        'end': [1, 2],
        'score': [[0.2, 0.7, 0.3], [0.1, 0.4, 0.8]]
    }
    threshold = 0.5
    expected_output = pd.DataFrame({
        'filename': ['file1', 'file2'],
        'start': [0, 1],
        'end': [1, 2],
        'label': [1, 2],
        'score': [0.7, 0.8]
    })
    pd.testing.assert_frame_equal(filter_by_threshold(detections, threshold), expected_output)

def test_filter_by_threshold_filter_with_scores_below_threshold():
    detections = {
        'filename': ['file1', 'file2'],
        'start': [0, 1],
        'end': [1, 2],
        'score': [[0.2, 0.4, 0.3], [0.1, 0.4, 0.2]]
    }
    threshold = 0.5
    expected_output = pd.DataFrame({
        'filename': [],
        'start': [],
        'end': [],
        'label': [],
        'score': []
    })
    pd.testing.assert_frame_equal(filter_by_threshold(detections, threshold), expected_output)

def test_filter_by_threshold_filter_with_empty_detections():
    detections = {
        'filename': [],
        'start': [],
        'end': [],
        'score': []
    }
    threshold = 0.5
    expected_output = pd.DataFrame({
        'filename': [],
        'start': [],
        'end': [],
        'label': [],
        'score': []
    })
    pd.testing.assert_frame_equal(filter_by_threshold(detections, threshold), expected_output)



def test_convert_sequence_to_snapshot_empty_input():
    detections = {'filename': [], 'start': [], 'end': [], 'score': []}
    df = convert_sequence_to_snapshot(detections)
    assert df.empty

def test_convert_sequence_to_snapshot_single_event_above_threshold():
    detections = {
        'filename': ['file1.wav'],
        'start': [0.0],
        'end': [60.0],
        'score': [[[0.1, 0.6, 0.4], [0.2, 0.3, 0.5]]]
    }
    df = convert_sequence_to_snapshot(detections, 0.5)
    expected_df = pd.DataFrame({
        'filename': ['file1.wav'], 
        'start': [20.0], 
        'end': [40.0], 
        'label': [0], 
        'score': [[0.6]]
    })
    pd.testing.assert_frame_equal(df, expected_df, check_exact=False, atol=1e-5)

def test_convert_sequence_to_snapshot_multiple_events_highest_score_only():
    detections = {
        'filename': ['file1.wav'],
        'start': [0.0],
        'end': [60.0],
        'score': [[[0.8, 0.9, 0.7, 0.2, 0.1, 0.6, 0.9, 0.9, 0.2], [0.7, 0.4, 0.6, 0.8, 0.6, 0.7, 0.8, 0.6, 0.1]]]
    }
    df = convert_sequence_to_snapshot(detections, 0.5, highest_score_only=True)
    expected_df = pd.DataFrame({
        'filename': ['file1.wav', 'file1.wav', 'file1.wav'], 
        'start': [0.0, 20.0, 40.0], 
        'end': [20.0, 40.0, 53.33333], 
        'label': [0, 1, 0], 
        'score': [[0.8, 0.9, 0.7], [0.8, 0.6, 0.7], [0.9, 0.9]]
    })
    pd.testing.assert_frame_equal(df, expected_df, check_exact=False, atol=1e-5)

def test_convert_sequence_to_snapshot_single_event_below_threshold():
    detections = {
        'filename': ['file1.wav'],
        'start': [0.0],
        'end': [60.0],
        'score': [[[0.1, 0.3, 0.4], [0.2, 0.3, 0.4]]]
    }
    df = convert_sequence_to_snapshot(detections, 0.5)
    assert df.empty

def test_convert_sequence_to_snapshot_single_event_at_threshold():
    detections = {
        'filename': ['file1.wav'],
        'start': [0.0],
        'end': [60.0],
        'score': [[[0.5, 0.3, 0.4], [0.2, 0.3, 0.4]]]
    }
    df = convert_sequence_to_snapshot(detections, 0.5)
    assert df.empty

def test_convert_sequence_to_snapshot_multiple_files():
    detections = {
        'filename': ['file1.wav', 'file2.wav'],
        'start': [0.0, 0.0],
        'end': [60.0, 60.0],
        'score': [
            [[0.5, 0.3, 0.4], [0.2, 0.3, 0.4]],
            [[0.7, 0.6, 0.8], [0.5, 0.4, 0.2]]
        ]
    }
    df = convert_sequence_to_snapshot(detections, 0.5)
    expected_df = pd.DataFrame({
        'filename': ['file2.wav'], 
        'start': [0.0, ], 
        'end': [60.0], 
        'label': [0], 
        'score': [[0.7, 0.6, 0.8]]
    })
    pd.testing.assert_frame_equal(df, expected_df, check_exact=False, atol=1e-5)

def test_convert_sequence_to_snapshot_different_start_end_times():
    detections = {
        'filename': ['file1.wav'],
        'start': [10.0],
        'end': [50.0],
        'score': [[[0.1, 0.6, 0.4], [0.2, 0.3, 0.5]]]
    }
    df = convert_sequence_to_snapshot(detections, 0.5)
    expected_df = pd.DataFrame({
        'filename': ['file1.wav'], 
        'start': [23.33333], 
        'end': [36.66666], 
        'label': [0], 
        'score': [[0.6]]
    })
    pd.testing.assert_frame_equal(df, expected_df, check_exact=False, atol=1e-5)

def test_merge_overlapping_detections_empty_input():
    """Test with an empty input dataframe."""
    empty_df = pd.DataFrame(columns=['filename', 'start', 'end', 'label', 'score'])
    assert merge_overlapping_detections(empty_df).equals(empty_df)

def test_merge_overlapping_detections_single_detection():
    """Test with a single detection in the input dataframe."""
    single_detection_df = pd.DataFrame([{'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1}])
    assert merge_overlapping_detections(single_detection_df).equals(single_detection_df)

def test_merge_overlapping_detections_no_overlap():
    """Test with multiple detections that do not overlap or are adjacent."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1},
        {'filename': 'file1', 'start': 6, 'end': 10, 'label': 1, 'score': 2}
    ])
    assert merge_overlapping_detections(input_df).equals(input_df)

def test_merge_overlapping_detections_adjacent_detections():
    """Test with adjacent detections that should be merged."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1},
        {'filename': 'file1', 'start': 5, 'end': 10, 'label': 0, 'score': 2}
    ])
    expected_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 10, 'label': 0, 'score': 1.5}
    ])
    assert merge_overlapping_detections(input_df).equals(expected_df)

def test_merge_overlapping_detections_overlapping_detections():
    """Test with overlapping detections that should be merged."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1},
        {'filename': 'file1', 'start': 3, 'end': 10, 'label': 0, 'score': 2}
    ])
    expected_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 10, 'label': 0, 'score': 1.5}
    ])
    assert merge_overlapping_detections(input_df).equals(expected_df)

def test_merge_overlapping_detections_multiple_detections():
    """Test with multiple detections in different files, some of which overlap and/or are adjacent."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1},
        {'filename': 'file1', 'start': 3, 'end': 7, 'label': 0, 'score': 2},
        {'filename': 'file1', 'start': 8, 'end': 12, 'label': 1, 'score': 3},
        {'filename': 'file1', 'start': 10, 'end': 15, 'label': 1, 'score': 4},
        {'filename': 'file2', 'start': 0, 'end': 5, 'label': 2, 'score': 5},
        {'filename': 'file2', 'start': 5, 'end': 10, 'label': 2, 'score': 6}
    ])
    expected_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 7, 'label': 0, 'score': 1.5},
        {'filename': 'file1', 'start': 8, 'end': 15, 'label': 1, 'score': 3.5},
        {'filename': 'file2', 'start': 0, 'end': 10, 'label': 2, 'score': 5.5}
    ])
    assert merge_overlapping_detections(input_df).equals(expected_df)

def test_merge_overlapping_detections_sequence_scores():
    """Test with multiple detections that have sequence of score."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 'dog', 'score': [1,2,3,4,5,6]},
        {'filename': 'file1', 'start': 4, 'end': 10, 'label': 'dog', 'score': [2,3,4,5,6,7,8]}
    ])

    result = merge_overlapping_detections(input_df)
    expected_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 10, 'label': 'dog', 'score': [1,2,3,4,3.5,4.5,4,5,6,7,8]}
    ])
    assert result.equals(expected_df)

def test_merge_overlapping_detections_multiple_sequence_scores():
    """Test with multiple detections in different files that have sequence of score."""
    input_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'label': 'dog', 'score': [1,2,3,4,5,6]},
        {'filename': 'file1', 'start': 4, 'end': 7, 'label': 'dog', 'score': [2,3,4,5]},
        {'filename': 'file2', 'start': 0, 'end': 5, 'label': 'bird', 'score': [5,6,7,8,9,10]},
        {'filename': 'file2', 'start': 4, 'end': 8, 'label': 'bird', 'score': [6,7,8,9,10]}
    ])

    result = merge_overlapping_detections(input_df)
    expected_df = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 7, 'label': 'dog', 'score': [1,2,3,4,3.5,4.5,4,5]},
        {'filename': 'file2', 'start': 0, 'end': 8, 'label': 'bird', 'score': [5,6,7,8,7.5,8.5,8,9,10]}
    ])
    assert result.equals(expected_df)

def test_merge_consecutive_detections_empty_dataframe():
    detections_df = pd.DataFrame(columns=['filename', 'start', 'end', 'score'])
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)
    assert result.empty

def test_merge_consecutive_detections_single_detection():
    detections_df = pd.DataFrame({
        'filename': ['file1'],
        'start': [0.0],
        'end': [3.0],
        'label': [1],
        'score': [0.8]
    })
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)
    assert len(result) == 1
    assert result.iloc[0]['start'] == 0.0
    assert result.iloc[0]['end'] == 2.0
    assert result.iloc[0]['score'] == 0.8


def test_merge_consecutive_detections_negative_step_size():
    """Test that a ValueError is raised when step_size is negative."""
    df = pd.DataFrame({
        'filename': ['file1', 'file1', 'file2', 'file2'],
        'start': [0.0, 2.0, 0.0, 10.0],
        'end': [3.0, 5.0, 3.0, 13.0],
        'score': [0.8, 0.6, 0.9, 0.7]
    })

    with pytest.raises(ValueError) as excinfo:
        merge_consecutive_detections(df, -1.0)

    assert str(excinfo.value) == 'step_size must be non-negative'


def test_merge_consecutive_detections_continuous_scores():
    detections_df = pd.DataFrame({
        'filename': ['file1', 'file1'],
        'start': [0.0, 2.0],
        'end': [3.0, 5.0],
        'label': [1, 1],
        'score': [[0.8, 0.6], [0.2, 0.4]]
    })
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)
    assert len(result) == 1
    assert result.iloc[0]['start'] == 0.0
    assert result.iloc[0]['end'] == 4.0
    assert result.iloc[0]['score'] == [0.5, 0.5]

def test_merge_consecutive_detections_multiple_detections():
    detections_df = pd.DataFrame({
        'filename': ['file1', 'file1'],
        'start': [0.0, 2.0],
        'end': [3.0, 5.0],
        'label': [1, 1],
        'score': [0.8, 0.6]
    })
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)
    assert len(result) == 1
    assert result.iloc[0]['start'] == 0.0
    assert result.iloc[0]['end'] == 4.0
    assert result.iloc[0]['score'] == 0.7

def test_merge_consecutive_detections_non_consecutive_detections():
    detections_df = pd.DataFrame({
        'filename': ['file1', 'file1'],
        'start': [0.0, 4.0],
        'end': [3.0, 7.0],
        'label': [1, 1],
        'score': [0.8, 0.6]
    })
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)

    assert len(result) == 2
    assert result.iloc[0]['start'] == 0.0
    assert result.iloc[0]['end'] == 2.0
    assert result.iloc[0]['score'] == 0.8
    assert result.iloc[1]['start'] == 4.0
    assert result.iloc[1]['end'] == 6.0
    assert result.iloc[1]['score'] == 0.6

def test_merge_consecutive_detections_mixed_consecutive_and_non_consecutive_detections():
    detections_df = pd.DataFrame({
        'filename': ['file1', 'file1', 'file1', 'file2'],
        'start': [0.0, 2.0, 4.0, 0.0],
        'end': [3.0, 5.0, 7.0, 3.0],
        'label': [1, 1, 1, 1],
        'score': [0.9, 0.8, 0.7, 0.7]
    })
    step_size = 2.0
    result = merge_consecutive_detections(detections_df, step_size)

    expected_df = pd.DataFrame({
        'filename': ['file1', 'file2'],
        'start': [0.0, 0.0],
        'end': [6.0, 2.0],
        'label': [1, 1],
        'score': [0.8, 0.7]
    })
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

def test_add_detection_buffer():
    buffer = 1.0

    orig_detection = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 5, 'score': 1},
        {'filename': 'file1', 'start': 3, 'end': 7, 'score': 2},
        {'filename': 'file2', 'start': 0, 'end': 5, 'score': 3}
    ])

    expected_detections = pd.DataFrame([
        {'filename': 'file1', 'start': 0, 'end': 6.0, 'score': 1},
        {'filename': 'file1', 'start': 2.0, 'end': 8.0, 'score': 2},
        {'filename': 'file2', 'start': 0, 'end': 6.0, 'score': 3}
    ])
    
    result = add_detection_buffer(orig_detection, buffer)
    
    pd.testing.assert_frame_equal(result, expected_detections)
    assert (result['start'] >= 0).all()  # Check that all start times are non-negative

def test_batch_load_audio_file_data():
    # Mock an AudioFrameLoader object
    loader = MagicMock(spec=AudioFrameLoader)

    # Mock the loader's num() method to return 10
    loader.num.return_value = 10

    # Mock the loader's next() method to return mock spectrogram data, filename, start, and duration
    mock_spec = Mock()
    mock_spec.get_data.return_value = 'mock_spectrogram_data'
    mock_spec.filename = 'mock_filename'
    mock_spec.start = 0
    mock_spec.duration.return_value = 5
    loader.__next__.side_effect = [mock_spec for _ in range(10)]

    # Call the function with the mock loader and batch_size=5
    batches = list(batch_load_audio_file_data(loader, batch_size=5))

    # There should be 2 batches
    assert len(batches) == 2

    # Check the contents of the first batch
    batch1 = batches[0]
    assert np.array_equal(batch1['data'], ['mock_spectrogram_data'] * 5)
    assert batch1['filename'] == ['mock_filename'] * 5
    assert batch1['start'] == [0] * 5
    assert batch1['end'] == [5] * 5

    # Check the contents of the second batch
    batch2 = batches[1]
    assert np.array_equal(batch2['data'], ['mock_spectrogram_data'] * 5)
    assert batch2['filename'] == ['mock_filename'] * 5
    assert batch2['start'] == [0] * 5
    assert batch2['end'] == [5] * 5

   
    # Check that the loader's num() method was called three times
    assert loader.num.call_count == 3


def test_batch_load_audio_file_data_single_batch():
    # Mock an AudioFrameLoader object
    loader = MagicMock(spec=AudioFrameLoader)

    # Mock the loader's num() method to return 3
    loader.num.return_value = 3

    # Mock the loader's next() method to return mock spectrogram data, filename, start, and duration
    mock_spec = Mock()
    mock_spec.get_data.return_value = 'mock_spectrogram_data'
    mock_spec.filename = 'mock_filename'
    mock_spec.start = 0
    mock_spec.duration.return_value = 5
    loader.__next__.side_effect = [mock_spec for _ in range(3)]

    # Call the function with the mock loader and batch_size=5
    batches = list(batch_load_audio_file_data(loader, batch_size=5))

    # There should be 1 batch
    assert len(batches) == 1

    # Check the contents of the batch
    batch = batches[0]
    np.array_equal(batch['data'], ['mock_spectrogram_data'] * 3)
    assert batch['filename'] == ['mock_filename'] * 3
    assert batch['start'] == [0] * 3
    assert batch['end'] == [5] * 3


def test_batch_load_audio_file_data_no_data():
    # Mock an AudioFrameLoader object
    loader = Mock(spec=AudioFrameLoader)

    # Mock the loader's num() method to return 0
    loader.num.return_value = 0

    # Call the function with the mock loader and batch_size=5
    batches = list(batch_load_audio_file_data(loader, batch_size=5))

    # There should be no batches
    assert len(batches) == 0


def test_batch_load_audio_file_data_varied_duration():
    # Mock an AudioFrameLoader object
    loader = MagicMock(spec=AudioFrameLoader)

    # Mock the loader's num() method to return 2
    loader.num.return_value = 2

    # Create two mock spectrograms with different durations
    mock_spec1 = Mock()
    mock_spec1.get_data.return_value = 'mock_spectrogram_data1'
    mock_spec1.filename = 'mock_filename1'
    mock_spec1.start = 0
    mock_spec1.duration.return_value = 5

    mock_spec2 = Mock()
    mock_spec2.get_data.return_value = 'mock_spectrogram_data2'
    mock_spec2.filename = 'mock_filename2'
    mock_spec2.start = 5
    mock_spec2.duration.return_value = 10

    loader.__next__.side_effect = [mock_spec1, mock_spec2]

    # Call the function with the mock loader and batch_size=2
    batches = list(batch_load_audio_file_data(loader, batch_size=2))

    # There should be 1 batch
    assert len(batches) == 1

    # Check the contents of the batch
    batch = batches[0]
    assert np.array_equal(batch['data'], ['mock_spectrogram_data1', 'mock_spectrogram_data2'])
    assert batch['filename'] == ['mock_filename1', 'mock_filename2']
    assert batch['start'] == [0, 5]
    assert batch['end'] == [5, 15]  # end is start + duration

def test_batch_load_audio_file_data_with_error_and_logger():
    # Mock an AudioFrameLoader object
    loader = MagicMock(spec=AudioFrameLoader)

    # Mock the loader's num() method to return 2
    loader.num.return_value = 2

    # Mock the loader's next() method to return a valid spectrogram and then raise an exception
    mock_spec = Mock()
    mock_spec.get_data.return_value = 'mock_spectrogram_data'
    mock_spec.filename = 'mock_filename'
    mock_spec.start = 0
    mock_spec.duration.return_value = 5
    loader.__next__.side_effect = [mock_spec, Exception("mock error message")]

    # Mock a logger
    logger = MagicMock(spec=KetosLogger)

    # Call the function with the mock loader and logger, and batch_size=2
    batches = list(batch_load_audio_file_data(loader, batch_size=2, logger=logger))

    # There should be 1 batch (the second batch is skipped because of the error)
    assert len(batches) == 1

    # Check the contents of the batch
    batch = batches[0]
    assert np.array_equal(batch['data'], ['mock_spectrogram_data'])
    assert batch['filename'] == ['mock_filename']
    assert batch['start'] == [0]
    assert batch['end'] == [5]

    # Check that the logger's error() method was called with the expected message
    logger.error.assert_called_once_with("mock error message Skipping File.", stdout=True, status='error')

