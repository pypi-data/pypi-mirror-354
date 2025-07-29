# ================================================================================ #
#   Authors: Bruno Padovese, Fabio Frazao and Oliver Kirsebom                      #
#   Contact: bpadovese@dal.ca, fsfrazao@dal.ca, oliver.kirsebom@dal.ca             #
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

import pandas as pd
import pytest
from ketos.data_handling.annotations_handling import standardize, adjust_segment_interval, generate_time_shifted_segments, validate_segment, create_random_segments
import numpy as np

# Sample DataFrames for testing
data1 = {'filename': ['file1.wav', 'file2.wav', 'file1.wav'],
         'label': ['A', 'B', 'A'],
         'start': [0, 10, 5],
         'end': [5, 15, 10]}
df1 = pd.DataFrame(data1)

data2 = {'filename': ['file1.wav', 'file2.wav'],
         'label': [1, 2],
         'start': [0, 10]}
df2 = pd.DataFrame(data2)

data3 = {'file': ['file1.wav', 'file2.wav'],
         'label': ['C', 'D']}
df3 = pd.DataFrame(data3)

data4 = {'filename': ['file1.wav', 'file2.wav'],
         'category': ['E', 'F']}
df4 = pd.DataFrame(data4)

data5 = {'filename': ['file1.wav', 'file2.wav', 'file3.wav'],
         'label': ['A', 'B', 'C']}
df5 = pd.DataFrame(data5)


######################## Standardize Function #######################

def test_standardize_from_dataframe_auto():
    df = standardize(df1)
    assert isinstance(df, pd.DataFrame)
    assert 'label' in df.columns
    assert df.attrs['label_dict'] == {'A': 0, 'B': 1}
    assert df['label'].dtype == int
    assert list(df['label']) == [0, 0, 1]
    assert list(df['filename']) == ['file1.wav', 'file1.wav', 'file2.wav']
    assert list(df['start']) == [0, 5, 10]

def test_standardize_from_dataframe_list():
    df = standardize(df1, labels=['B', 'A'])
    assert df.attrs['label_dict'] == {'B': 0, 'A': 1}
    assert list(df['label']) == [1, 1, 0]

def test_standardize_from_dataframe_dict():
    label_map = {'A': 10, 'B': 20}
    df = standardize(df1, labels=label_map)
    assert df.attrs['label_dict'] == label_map
    assert list(df['label']) == [10, 10, 20]

def test_standardize_from_dataframe_none():
    df = standardize(df2, labels=None)
    assert df.attrs['label_dict'] == {}
    assert list(df['label']) == [1, 2]

def test_standardize_from_csv(tmp_path):  # Use tmp_path for temporary files
    csv_file = tmp_path / "test.csv"
    df1.to_csv(csv_file, index=False)
    df = standardize(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert 'label' in df.columns
    assert df.attrs['label_dict'] == {'A': 0, 'B': 1}
    assert list(df['label']) == [0, 0, 1]

def test_standardize_missing_columns():
    with pytest.raises(AssertionError) as excinfo:
        standardize(df3)
    assert "Missing required column(s): filename" in str(excinfo.value)
    with pytest.raises(AssertionError) as excinfo:
        standardize(df4)
    assert "Missing required column(s): label" in str(excinfo.value)

def test_standardize_invalid_labels_type():
    with pytest.raises(ValueError) as excinfo:
        standardize(df1, labels="invalid")
    assert "Unsupported value for labels argument" in str(excinfo.value)

def test_standardize_invalid_input_type():
    with pytest.raises(ValueError) as excinfo:
        standardize(123)
    assert "Annotations must be a pandas DataFrame or a file path to a CSV file." in str(excinfo.value)

def test_standardize_sort_by_filename_and_start():
    df = standardize(df1)
    assert list(df['filename']) == ['file1.wav', 'file1.wav', 'file2.wav']
    assert list(df['start']) == [0, 5, 10]

def test_standardize_fillna_minus_one():
    df = standardize(df5, labels=["A", "B"])
    assert list(df['label']) == [0, 1, -1]

def test_standardize_sep_argument(tmp_path):
    data_sep = {'filename': ['file1.wav;file2.wav'],
                 'label': ['A;B']}
    df_sep = pd.DataFrame(data_sep)
    csv_file = tmp_path / "test_sep.csv"
    df_sep.to_csv(csv_file, index=False, sep=';')
    df = standardize(str(csv_file), sep=';')
    assert isinstance(df, pd.DataFrame)
    assert df.attrs['label_dict'] == {'A;B':0}


    ######################## adjust_segment_interval Function #######################

@pytest.mark.parametrize(
    "duration, expected_start, expected_end",
    [
        (3.0, [1.0, 11.0, 21.0], [4.0, 14.0, 24.0]),
        (1.0, [2.0, 12.0, 22.0], [3.0, 13.0, 23.0]),  # Example with a different duration
    ],
)
def test_adjust_segment_interval_centered(duration, expected_start, expected_end):
    """Test the function with `center=True` using parametrization."""
    data = {'start': [0, 10, 20], 'end': [5, 15, 25]}
    df = pd.DataFrame(data)

    result = adjust_segment_interval(df, duration=duration, center=True)

    assert result['start'].tolist() == expected_start
    assert result['end'].tolist() == expected_end

def test_adjust_segment_interval_random():
    """Test the function with `center=False` to randomly place segments."""
    data = {'start': [0, 10, 20], 'end': [5, 15, 25]}
    df = pd.DataFrame(data)
    duration = 3.0

    result = adjust_segment_interval(df, duration=duration, center=False)

    # Verify the duration is maintained
    assert all((result['end'] - result['start']).round(6) == duration)

    # Verify random placement stays within bounds
    for idx, row in result.iterrows():
        original_start = data['start'][idx]
        original_end = data['end'][idx]
        assert original_start <= row['start'] <= original_end - duration

def test_adjust_segment_interval_boundary_conditions():
    """Test boundary conditions where start or end times are near 0."""
    data = {'start': [0, 2, 5], 'end': [5, 7, 10]}
    df = pd.DataFrame(data)
    duration = 3.0

    result = adjust_segment_interval(df, duration=duration, center=True)

    # Verify centralization does not go below 0
    assert all(result['start'] >= 0)

def test_adjust_segment_interval_large_duration():
    """Test behavior when duration is larger than original intervals."""
    data = {'start': [0, 10, 20], 'end': [5, 15, 25]}
    df = pd.DataFrame(data)
    duration = 10.0

    result = adjust_segment_interval(df, duration=duration, center=True)

    # Verify start is capped at 0 for the first row
    assert result.loc[0, 'start'] == 0
    assert all((result['end'] - result['start']).round(6) == duration)

def test_adjust_segment_interval_empty_dataframe():
    """Test the function with an empty DataFrame."""
    df = pd.DataFrame(columns=['start', 'end'])
    duration = 3.0

    result = adjust_segment_interval(df, duration=duration, center=True)

    # Verify the result is still empty
    assert result.empty

def test_adjust_segment_interval_invalid_columns():
    """Test the function with a DataFrame missing required columns."""
    df = pd.DataFrame({'start': [0, 10, 20]})  # Missing 'end' column
    duration = 3.0

    with pytest.raises(KeyError):
        adjust_segment_interval(df, duration=duration, center=True)

def test_adjust_segment_interval_random_consistency():
    """Test random placement consistency by setting a seed."""
    data = {'start': [0, 10, 20], 'end': [5, 15, 25]}
    df = pd.DataFrame(data)
    duration = 3.0

    np.random.seed(42)  # Set random seed
    result1 = adjust_segment_interval(df, duration=duration, center=False)

    np.random.seed(42)  # Reset random seed
    result2 = adjust_segment_interval(df, duration=duration, center=False)

    # Verify both results are identical due to seed consistency
    pd.testing.assert_frame_equal(result1, result2)

    ######################## generate_time_shifted_segments Function #######################

def test_time_shifted_segments_default():
    """Test default behavior with basic inputs."""
    data = {'start': [0, 10], 'end': [5, 15]}
    df = pd.DataFrame(data)
    step = 1.0
    duration = 3.0

    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)

    # Verify the output contains shifted segments
    assert not result.empty
    assert all((result['end'] - result['start']).round(6) == duration)
    
    # Check that no central annotation is included by default
    for _, original_row in df.iterrows():
        assert not any(
            (result['start'] == original_row['start']) & (result['end'] == original_row['end'])
        ), f"Original segment found in shifted results: {original_row}"

def test_time_shifted_segments_min_overlap_zero():
    """Test that a ValueError is raised when min_overlap is 0."""

    # Test DataFrame with annotations
    data = {'start': [0, 10], 'end': [5, 15]}  # Example annotations
    df = pd.DataFrame(data)

    # Parameters
    step = 1
    duration = 3
    min_overlap = 0  # Invalid value
    include_unshifted = True

    # Expect a ValueError to be raised
    with pytest.raises(ValueError, match="min_overlap must be greater than 0 and less than or equal to 1."):
        generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=min_overlap, include_unshifted=include_unshifted)

def test_time_shifted_segments_include_unshifted():
    """Test including the central annotation."""
    data = {'start': [0, 10], 'end': [5, 15]}
    df = pd.DataFrame(data)
    step = 1.0
    duration = 3.0

    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5, include_unshifted=True)

    # Verify the central annotation is included
    assert len(result[result['start'] == 0]) > 0
    assert len(result[result['start'] == 10]) > 0

@pytest.mark.parametrize(
    "min_overlap, expected_result",
    [
        (1.0, []),  # Expecting an empty DataFrame since a 3-second segment can never fully overlap a 5-second annotation with a min_overlap of 1.0
        (0.5, [
            {"start": 0, "end": 3}, {"start": 1, "end": 4}, {"start": 2, "end": 5},  # Valid segments for first annotation
            {"start": 10, "end": 13}, {"start": 11, "end": 14}, {"start": 12, "end": 15}  # Valid segments for second annotation
        ]),
        (0.1, [
            {"start": -2, "end": 1}, {"start": -1, "end": 2}, {"start": 0, "end": 3}, {"start": 1, "end": 4}, {"start": 2, "end": 5}, {"start": 3, "end": 6}, {"start": 4, "end": 7},  # Includes additional shifts
            {"start": 8, "end": 11}, {"start": 9, "end": 12}, {"start": 10, "end": 13}, {"start": 11, "end": 14}, {"start": 12, "end": 15}, {"start": 13, "end": 16}, {"start": 14, "end": 17}
        ])
    ]
)
def test_time_shifted_segments_min_duration_smaller_than_original_length(min_overlap, expected_result):
    """Test behavior when the original length of the annotation is bigger than the duration parameter."""
    # Test DataFrame with annotations longer than the duration parameter
    data = {'start': [0, 10], 'end': [5, 15]}  # Original annotations (length = 5 seconds each)
    df = pd.DataFrame(data)

    # Parameters
    step = 1
    duration = 3  # Shorter than the original annotation length
    include_unshifted = True

    # Call the function
    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=min_overlap, include_unshifted=include_unshifted)

    # Convert result to a comparable format (list of dictionaries for easy checking)
    result_dicts = result.to_dict(orient="records")

    # Assertions
    assert result_dicts == expected_result, f"Failed for min_overlap={min_overlap}: {result_dicts}"

@pytest.mark.parametrize(
    "min_overlap, expected_result",
    [
        (1.0, [
            {'start': -2, 'end': 5}, {'start': -1, 'end': 6}, {"start": 0, "end": 7},  # Fully overlapping segments for first annotation
            {'start': 8, 'end': 15}, {'start': 9, 'end': 16}, {"start": 10, "end": 17} # Fully overlapping segments for second annotation
        ]),
        (0.5, [
            {'start': -4, 'end': 3}, {'start': -3, 'end': 4}, {'start': -2, 'end': 5}, {'start': -1, 'end': 6}, {"start": 0, "end": 7}, {"start": 1, "end": 8}, {"start": 2, "end": 9},
            {'start': 6, 'end': 13}, {'start': 7, 'end': 14}, {'start': 8, 'end': 15}, {'start': 9, 'end': 16}, {"start": 10, "end": 17}, {"start": 11, "end": 18}, {"start": 12, "end": 19}
        ]),
        (0.1, [
            {'start': -5, 'end': 2}, {'start': -4, 'end': 3}, {"start": -3, "end": 4}, {"start": -2, "end": 5}, {"start": -1, "end": 6}, {"start": 0, "end": 7}, {"start": 1, "end": 8}, {"start": 2, "end": 9}, {"start": 3, "end": 10},
            {'start': 4, 'end': 11}, {'start': 5, 'end': 12}, {'start': 6, 'end': 13},{"start": 7, "end": 14}, {"start": 8, "end": 15}, {"start": 9, "end": 16}, {"start": 10, "end": 17}, {"start": 11, "end": 18}, {"start": 12, "end": 19}, {"start": 13, "end": 20}, {'start': 14, 'end': 21}
        ])
    ]
)
def test_time_shifted_segments_duration_longer_than_annotation(min_overlap, expected_result):
    """Test behavior when the duration parameter is bigger than the original annotation length."""

    # Test DataFrame with shorter annotations
    data = {'start': [0, 10], 'end': [5, 15]}  # Original annotations (length = 5 seconds each)
    df = pd.DataFrame(data)

    # Parameters
    step = 1
    duration = 7  # Longer than the original annotation length
    include_unshifted = True

    # Call the function
    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=min_overlap, include_unshifted=include_unshifted)

    # Convert result to a comparable format (list of dictionaries for easy checking)
    result_dicts = result.to_dict(orient="records")

    # Assertions
    assert result_dicts == expected_result, f"Failed for min_overlap={min_overlap}: {result_dicts}"

def test_time_shifted_segments_large_step():
    """Test behavior with a large step size."""
    data = {'start': [0], 'end': [10]}
    df = pd.DataFrame(data)
    step = 5.0
    duration = 5.0

    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)

    # Verify fewer segments are generated with a large step
    assert len(result) == 2  # Only two shifts are possible: -5 and +5

def test_time_shifted_segments_no_duration():
    """Test with duration=None to use original annotation durations."""
    data = {'start': [0, 10], 'end': [5, 15]}
    df = pd.DataFrame(data)
    step = 1.0

    result = generate_time_shifted_segments(df, step=step, duration=None, min_overlap=0.5)

    # Verify the original annotation durations are maintained
    assert all((result['end'] - result['start']) == (df['end'] - df['start']).iloc[0])

def test_time_shifted_segments_out_of_bounds():
    """Test handling of out-of-bounds start and end times."""
    data = {'start': [5], 'end': [10]}
    df = pd.DataFrame(data)
    step = 1.0
    duration = 5.0

    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)

    # Verify the segments can extend beyond original bounds
    assert result['start'].min() < 5
    assert result['end'].max() > 10

def test_time_shifted_segments_empty_dataframe():
    """Test with an empty DataFrame."""
    df = pd.DataFrame(columns=['start', 'end'])
    step = 1.0
    duration = 3.0

    result = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)
    
    # Verify the result is empty
    assert result.empty

def test_time_shifted_segments_invalid_overlap():
    """Test invalid overlap values."""
    df = pd.DataFrame({'start': [0], 'end': [10]})
    step = 1.0
    duration = 3.0

    with pytest.raises(ValueError, match="min_overlap must be greater than 0 and less than or equal to 1."):
        generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=-0.5)

    with pytest.raises(ValueError, match="min_overlap must be greater than 0 and less than or equal to 1."):
        generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=1.5)

def test_time_shifted_segments_random_consistency():
    """Test random behavior consistency by setting a seed."""
    data = {'start': [0], 'end': [10]}
    df = pd.DataFrame(data)
    step = 1.0
    duration = 3.0

    np.random.seed(42)
    result1 = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)

    np.random.seed(42)
    result2 = generate_time_shifted_segments(df, step=step, duration=duration, min_overlap=0.5)

    # Verify results are identical due to fixed seed
    pd.testing.assert_frame_equal(result1, result2)

    ######################## create_random_segments Function #######################

def test_create_random_segments_no_valid_files():
    """Test behavior when no files are long enough for the duration and buffer."""
    files = pd.DataFrame({'filename': ['file1.wav'], 'duration': [4]})
    duration = 5
    buffer = 0.5
    result = create_random_segments(files, duration=duration, num=2, buffer=buffer)
    assert result.empty, "Expected an empty DataFrame when no files are valid"


def test_create_random_segments_no_annotations():
    """Test segment generation without annotations."""
    files = pd.DataFrame({'filename': ['file1.wav', 'file2.wav'], 'duration': [10, 20]})
    duration = 3
    num = 2
    buffer = 0.5
    result = create_random_segments(files, duration=duration, num=num, buffer=buffer)
    assert len(result) == num, "Expected the specified number of segments to be generated"
    assert all(result['end'] - result['start'] == duration), "Segments should have the specified duration"


def test_create_random_segments_with_annotations():
    """Test segment generation with annotations that require validation."""
    files = pd.DataFrame({'filename': ['file1.wav', 'file2.wav'], 'duration': [10, 20]})
    annotations = pd.DataFrame({'filename': ['file1.wav'], 'start': [2], 'end': [5]})
    duration = 3
    num = 1
    buffer = 1
    result = create_random_segments(files, duration=duration, num=num, annotations=annotations, buffer=buffer)
    assert len(result) == num, "Expected the specified number of segments to be generated"
    for _, row in result.iterrows():
        assert validate_segment(annotations, row['filename'], row['start'], row['end'], buffer), \
            "Generated segments should not overlap with annotations"


def test_create_random_segments_partial_files_valid():
    """Test behavior when some files are valid for segment generation."""
    files = pd.DataFrame({'filename': ['file1.wav', 'file2.wav'], 'duration': [4, 15]})
    duration = 5
    buffer = 0.5
    num = 2
    result = create_random_segments(files, duration=duration, num=num, buffer=buffer)
    assert len(result) == num, "Expected the specified number of segments to be generated"
    assert all(result['filename'] == 'file2.wav'), "Segments should only be generated from valid files"


def test_create_random_segments_weighted_sampling():
    """Test that longer files are more likely to be sampled."""
    np.random.seed(42)  # Set seed for reproducibility
    files = pd.DataFrame({'filename': ['short.wav', 'long.wav'], 'duration': [5, 20]})
    duration = 3
    num = 10
    buffer = 0.5
    result = create_random_segments(files, duration=duration, num=num, buffer=buffer)
    short_count = len(result[result['filename'] == 'short.wav'])
    long_count = len(result[result['filename'] == 'long.wav'])
    assert long_count > short_count, "Longer files should be sampled more frequently"


def test_create_random_segments_max_attempts():
    """Test behavior when max attempts per file are reached."""
    files = pd.DataFrame({'filename': ['file1.wav'], 'duration': [10]})
    annotations = pd.DataFrame({'filename': ['file1.wav'], 'start': [2], 'end': [8]})
    duration = 3
    buffer = 1
    num = 2
    max_attempts_per_file = 1
    result = create_random_segments(files, duration=duration, num=num, annotations=annotations, buffer=buffer, max_attempts_per_file=max_attempts_per_file)
    assert len(result) < num, "Not all segments should be generated if max attempts are reached"
    
    ######################## validate_segment Function #######################

def test_validate_segment_no_annotations():
    """Test behavior when no annotations are provided."""
    assert validate_segment(None, 'file1.wav', 0, 10) is True, "Should return True when annotations are None"

def test_validate_segment_no_overlap():
    """Test a segment that does not overlap with any annotations."""
    data = {'filename': ['file1.wav', 'file1.wav'], 'start': [0, 10], 'end': [5, 15]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 6, 9) is True, "Segment should not overlap"

def test_validate_segment_overlap():
    """Test a segment that overlaps with an annotation."""
    data = {'filename': ['file1.wav', 'file1.wav'], 'start': [0, 10], 'end': [5, 15]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 4, 6) is False, "Segment overlaps and should return False"

def test_validate_segment_with_buffer_overlap():
    """Test a segment that overlaps with an annotation considering a buffer."""
    data = {'filename': ['file1.wav'], 'start': [20], 'end': [25]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 26, 30, buffer=2) is False, "Buffer causes overlap and should return False"

def test_validate_segment_with_buffer_no_overlap():
    """Test a segment that does not overlap with an annotation considering a buffer."""
    data = {'filename': ['file1.wav'], 'start': [20], 'end': [25]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 26, 30, buffer=0.5) is True, "No overlap even with buffer"

def test_validate_segment_different_file():
    """Test behavior when segment belongs to a different file."""
    data = {'filename': ['file2.wav'], 'start': [0], 'end': [10]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 0, 10) is True, "Segment should not overlap as it's in a different file"

def test_validate_segment_multiple_annotations_no_overlap():
    """Test a segment that does not overlap with multiple annotations."""
    data = {'filename': ['file1.wav', 'file1.wav'], 'start': [0, 10], 'end': [5, 15]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 15, 20) is True, "Segment does not overlap with any annotations"

def test_validate_segment_multiple_annotations_overlap():
    """Test a segment that overlaps with one of multiple annotations."""
    data = {'filename': ['file1.wav', 'file1.wav'], 'start': [0, 10], 'end': [5, 15]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 8, 12) is False, "Segment overlaps with an annotation"

def test_validate_segment_edge_case_overlap():
    """Test a segment that starts and ends exactly at annotation boundaries."""
    data = {'filename': ['file1.wav'], 'start': [10], 'end': [20]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 10, 20) is False, "Segment exactly matches annotation boundaries and should return False"
    
def test_validate_segment_barely_no_overlap():
    """Test a segment that barely does not overlap with an annotation."""
    data = {'filename': ['file1.wav'], 'start': [10], 'end': [20]}
    annotations = pd.DataFrame(data)
    assert validate_segment(annotations, 'file1.wav', 8, 10) is True, "Segment ends exactly where annotation starts but does not overlap"
    assert validate_segment(annotations, 'file1.wav', 20, 22) is True, "Segment starts exactly where annotation ends but does not overlap"