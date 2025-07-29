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

""" detection sub-module within the ketos.neural_networks.dev_utils module

    This module provides auxiliary functions to incorporate pre-trained ketos classifiers models into detection tools

    Contents:
        

"""

import numpy as np
import pandas as pd
import os
import math
import warnings
import logging
import tables
from operator import itemgetter
from itertools import groupby
from tqdm import tqdm, trange
from scipy.ndimage import convolve

def compute_score_running_avg(scores, window_size):
    """
    This function calculates the running average of a given list of scores, over a defined window size.

    Each element i in the output represents the running average of the elements 
    in the scores from position i - window_size//2 to i + window_size//2.

    This function pads the scores with the edge values of input to calculate the average for the edges.
    
    Args:
        scores: list or numpy array
            A 1D, 2D or 3D sequence of numerical scores.
        window_size: int 
            The size of the window in frames to compute the running average. Must be an odd integer

    Returns:
        numpy array
            A sequence of running averages, with the same length as the input. 
    
    Example:

    >>> compute_score_running_avg([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)
    array([1.33333333, 2.        , 3.        , 4.        , 5.        ,
           6.        , 7.        , 8.        , 9.        , 9.66666667])

    >>> compute_score_running_avg([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]], 3)
    array([[1.33333333, 1.33333333],
           [2.        , 2.        ],
           [3.        , 3.        ],
           [4.        , 4.        ],
           [4.66666667, 4.66666667]])
    
    >>> np.random.seed(0)
    >>> scores = np.random.rand(6, 4)
    >>> compute_score_running_avg(scores, 3)
    array([[0.50709394, 0.69209095, 0.54770465, 0.66051312],
           [0.64537702, 0.58150833, 0.61069188, 0.6551837 ],
           [0.65178737, 0.65164409, 0.43344944, 0.50259907],
           [0.51730857, 0.713886  , 0.54697262, 0.49534546],
           [0.52229377, 0.85245835, 0.43689072, 0.57922354],
           [0.65915169, 0.81031232, 0.56703849, 0.81035683]])
    """

    if window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer")
    
    # Ensure scores is a numpy array for convenience
    scores = np.array(scores, dtype=float)
    
    # Check if window_size is larger than the length of input scores
    if window_size > scores.shape[0]:
        raise ValueError("window_size cannot be larger than the length of the input scores")

    
    # Ensure we have 3 or less dimensions
    if scores.ndim > 4:
        raise ValueError("scores must be a 1D, 2D or 3D list or array")

    weights = np.ones(window_size) / window_size
    # here we are creating the weights which can be viwed as doing the divison operation of calculating the avarage before actually summing the values
    # The weights will be applied to each input in the window and summed together in the convolution operation
    if scores.ndim == 1:
        return convolve(scores, weights, mode='nearest')
    elif scores.ndim == 2 or scores.ndim == 3:
        return np.apply_along_axis(convolve, axis=0, arr=scores, weights=weights, mode='nearest')
    else:
        raise ValueError("scores must be a 1D, 2D, or 3D list or array")

def batch_load_hdf5_data(hdf5_file_path, batch_size, audio_representation, start_idx=0, table_name=None, x_field='/data', logger=None):
    """
    Loads HDF5 data in batches from a specified file and yields it for processing.

    This function assumes that the HDF5 dataset is named 'data'. For each batch, it will yield a dictionary
    containing the batch's data, filename, start and end offsets.

    - The 'data' key in the yielded dictionary corresponds to the batch's data.
    - The 'filename' key in the yielded dictionary corresponds to the batch's filename.
    - The 'start' key in the yielded dictionary corresponds to the start offset of the batch.
    - The 'end' key in the yielded dictionary corresponds to the end offset of the batch.

    Args:
        hdf5_file_path : str
            The file path of the HDF5 file to read from.
        batch_size : int
            The number of samples to include in each batch.
        audio_representation : dict
            A dictionary containing information about the audio representation.
        start_idx: int
            The batch index to start from. This allows the generator to skip the initial batches up to the specified index.
        table_name : str
            The name of the table in the HDF5 file to read the data from.
            If no name is provided, it defaults to '/data'.
        x_field : str
            Name of the field in the table to access the data.
        logger: logging.Logger or KetosLogger
            A Logger instance to log errors encountered while loading audio file data.

    Returns:
        dict
            A dictionary containing the batch data, its filename, start and end offsets.
            The 'end' key value is calculated based on the 'duration' key of the audio_representation parameter
            and may not be accurate, as the duration might change when actually computing the representation.
    """
    if table_name is None:
        table_name = "/data"
    else:
        table_name = table_name + "/data"

    # Define a vectorized function to decode bytes to utf-8 strings
    decode_utf8 = np.vectorize(lambda x: x.decode('utf-8'))

    with tables.open_file(hdf5_file_path, 'r') as hdf5_file:
        # Assuming the dataset is named 'data'
        table = hdf5_file.get_node(table_name)
        num_samples = table.shape[0]
        num_batches = int(np.ceil(num_samples / batch_size))

        batch_data = {}
        for i in trange(start_idx, num_batches):
            try:
                start = i * batch_size
                # Here we are getting the num of samples in a batch. Usually it is the batch size except for the last batch which could be smaller
                end = min((i + 1) * batch_size, num_samples)
                hdf5_batch_data = table[start:end]

                batch_data['data'] = hdf5_batch_data[x_field]
                batch_data['filename'] = decode_utf8(hdf5_batch_data['filename'])
                batch_data['start'] = hdf5_batch_data['start']
                batch_data['end'] = hdf5_batch_data['start'] + audio_representation['duration'] # this isnt quite right because the duration may change when actually computing the representation
            except Exception as e:
                print(e)
                if logger is not None:
                    logger.error(f'{e} Skipping File.', stdout=True, **{'status': 'error'})
                continue  # Skip this iteration if an error occurred

            yield batch_data

def batch_load_audio_file_data(loader, batch_size, start_idx=0, logger=None):
    """
    This function generates batches of audio data from a given AudioFrameLoader.

    Each batch consists of spectrogram data, filename, start time and end time of each audio segment.
    The loader loads audio files, splits into smaller segments and convert them into spectrograms.

    Args:
        loader: ketos.audio.audio_loader.AudioFrameLoader
            An AudioFrameLoader object that computes spectrograms from the audio files as requested.
        batch_size: int 
            The number of samples to include in each batch.
        start_idx: int
            The batch index to start from. This allows the generator to skip the initial batches up to the specified index.
        logger: logging.Logger or KetosLogger
            A Logger instance to log errors encountered while loading audio file data.
            

    Returns:
        dict: A dictionary containing the batch data. The dictionary keys are 'data', 'filename', 
              'start', and 'end'. The 'data' field is a numpy array of shape (batch_size, time_bins, freq_bins), 
              where time_bins and freq_bins correspond to the shape of the spectrogram data.
              'filename' contains the list of filenames for the audio segments in the batch.
              'start' and 'end' are lists containing the start and end times (in seconds) of each audio segment.
    """
    n_batches = int(np.ceil(loader.num() / batch_size))

    # Skip the previously processed batches
    for _ in range(start_idx * batch_size):
        loader.skip()

    for batch_id in trange(start_idx, n_batches):
        # This will compute how many samples should be loaded in the batch. Normally it is the batch size, 
        # but in the case where the last batch is smaller than batch size we just load the necessary amount
        # Each sample is a segment created by the AudioFrameLoader
        num_samples = min(batch_size, loader.num() - batch_size * batch_id) 

        batch_data = {"data": [], "filename": [], "start": [], "end": []}
        for _ in range(num_samples):
            try:
                spec = next(loader)

                # for some reason, the actual spectrogram data is found in data.data We should change this at some point
                # Batch data will be a list with length batch_size with each item beeing a np.array with shape (time_bins, freq_bins)
                batch_data['data'].append(spec.get_data()) 
                batch_data['filename'].append(spec.filename)
                batch_data['start'].append(spec.start)
                batch_data['end'].append(spec.start + float(spec.duration()))
            except Exception as e:
                if logger is not None:
                    logger.error(f'{e} Skipping File.', stdout=True, **{'status': 'error'})
                continue  # Skip this iteration if an error occurred
        # transform batch_data to be a numpy array with shape (batch_size, time_bins, freq_bins)
        batch_data['data'] = np.stack(batch_data['data'], axis=0) 
        yield batch_data

def add_detection_buffer(detections_df, buffer):
    """ Add a buffer to each detection in the DataFrame.

        Args:
            detections_df: pandas DataFrame
                DataFrame with detections. It should have the following columns:
                - 'filename': The name of the file containing the detection.
                - 'start': The start time of the detection in seconds.
                - 'end': The end time of the detection in seconds.
                - 'score': The score associated with the detection.
            buffer: float
                The buffer duration to be added to each detection in seconds.
        
        Returns:
            detections_df: pandas DataFrame
                DataFrame with the detections after adding the buffer.

        Example:
            Given a step_size of 0.5 and a DataFrame with the following format:

            +----------+-------+-----+-------+
            | filename | start | end | score |
            +----------+-------+-----+-------+
            | file1    | 1     | 3   | 0.9   |
            +----------+-------+-----+-------+
            | file2    | 0     | 2   | 0.8   |
            +----------+-------+-----+-------+

            The function would return:

            +----------+-------+-----+-------+
            | filename | start | end | score |
            +----------+-------+-----+-------+
            | file1    | 0.5   | 3.5 | 1.5   |
            +----------+-------+-----+-------+
            | file2    | 0     | 2.5 | 3     |
            +----------+-------+-----+-------+

        >>> import pandas as pd
        >>> detections_df = pd.DataFrame([
        ...     {'filename': 'file1', 'start': 1, 'end': 3, 'score': 0.9},
        ...     {'filename': 'file2', 'start': 0, 'end': 2, 'score': 0.8},
        ... ])
        >>> buffer = 0.5
        >>> add_detection_buffer(detections_df, buffer)
          filename  start  end  score
        0    file1    0.5  3.5    0.9
        1    file2    0.0  2.5    0.8

        >>> detections_df = pd.DataFrame([
        ...     {'filename': 'file1', 'start': 0, 'end': 5, 'score': 1.0},
        ...     {'filename': 'file2', 'start': 2, 'end': 4, 'score': 0.7},
        ... ])
        >>> buffer = 1.0
        >>> add_detection_buffer(detections_df, buffer)
          filename  start  end  score
        0    file1    0.0  6.0    1.0
        1    file2    1.0  5.0    0.7
    """
    detections_df_copy = detections_df.copy()

    detections_df_copy['start'] = detections_df_copy['start'].apply(lambda x: max(0, x - buffer)) # detection start cant be lower than 0
    detections_df_copy['end'] += buffer

    return detections_df_copy


def apply_detection_threshold(scores, threshold=0.5, highest_score_only=False):
    """
    Filters out detection scores below or at a specified threshold and returns a list of tuples, where each tuple consists of a label (the index of the score) and the score itself.
    
    Args:
        scores: list of floats
            The list of scores.
        threshold: float
            The threshold below which scores are filtered out. Default is 0.5.
        highest_score_only: bool
            If True, only the highest score is returned. Default is False.

    Returns:
        list of tuples: Each tuple contains a label (the index of the score in the input list) and the score itself.

    Examples:

    >>> apply_detection_threshold([0.2, 0.7, 0.3], 0.5)
    [(1, 0.7)]
    >>> apply_detection_threshold([0.6, 0.4, 0.8], 0.55)
    [(0, 0.6), (2, 0.8)]
    >>> apply_detection_threshold([0.6, 0.4, 0.8], 0.6, True)
    [(2, 0.8)]
    """

    filtered_scores = [(label, score) for label, score in enumerate(scores) if score >= threshold]
    
    if highest_score_only and filtered_scores:
        return [max(filtered_scores, key=lambda item: item[1])]
    else:
        return filtered_scores

def filter_by_threshold(detections, threshold=0.5, highest_score_only=False):
    """
    Filters out detection scores below a specified threshold and returns a DataFrame with the remaining detections. 
    
    Args:
        detections: dict
            The dictionary with the detections.
        threshold: float
            The threshold below which scores are filtered out. Default is 0.5.
        highest_score_only: bool
            If True, only the highest score is returned. Default is False.

    Returns:
        pd.DataFrame: DataFrame with the remaining detections.

    Examples:
    
    >>> detections = {
    ...    'filename': ['file1', 'file2'],
    ...    'start': [0, 1],
    ...    'end': [1, 2],
    ...    'score': [[0.2, 0.7, 0.3], [0.1, 0.4, 0.8]]
    ... }
    >>> filter_by_threshold(detections, 0.5)
      filename  start  end  label  score
    0    file1      0    1      1    0.7
    1    file2      1    2      2    0.8
    """
    # create an empty list to store the filtered output
    filtered_output = {'filename': [], 'start': [], 'end': [], 'label': [], 'score': []}

    for filename, start, end, scores in zip(detections['filename'], detections['start'], detections['end'], detections['score']):
        detections = apply_detection_threshold(scores, threshold, highest_score_only)
        # for each score that passes the threshold, duplicate the filename, start, end, and add the corresponding label
        # if there is no score above the threshold, exclude the segment from the 
        for label, score in detections:
            filtered_output['filename'].append(filename)
            filtered_output['start'].append(start)
            filtered_output['end'].append(end)
            filtered_output['label'].append(label)
            filtered_output['score'].append(float(score))
    df = pd.DataFrame(filtered_output)
    return df



def convert_sequence_to_snapshot(detections, threshold=0.5, highest_score_only=False):
    """
    Converts a sequence of scores into a snapshot of events that exceed a threshold.

    This assumes the output is from a sequence model. If using a snapshot model already, see :meth:`neural_networks.dev_utils.detection.filter_by_threshold`,
    
    The input data should be a dictionary containing:
      'filename': a list of filenames,
      'start': a list of start times for each input,
      'end': a list of end times for each input,
      'score': a 3D array or list of scores for each input, each sublist corresponding to a class.

    The output is a dictionary that contains:
      'filename': the filename where the event occurred,
      'start': the start time of the event,
      'end': the end time of the event,
      'label': the label of the class that triggered the event,
      'score': the scores of the class that triggered the event.

    Args:
        detections: dict
            A dictionary containing the filenames, start times, end times, and scores.
        threshold: float
            A threshold value to filter scores. Scores above this threshold are considered as an event. Default is 0.5.
        highest_score_only: bool
            If True, only the highest score is returned. Default is False.

    Returns:
        pandas.DataFrame: A DataFrame containing the snapshots of events.

    Examples:

    >>> data = {
    ...     'filename': ['file1.wav'],
    ...     'start': [0.0],
    ...     'end': [60.0],
    ...     'score': [[
    ...         [0.1, 0.6, 0.4],
    ...         [0.2, 0.3, 0.5]
    ...     ]]
    ... }
    >>> df = convert_sequence_to_snapshot(data, 0.5)
    >>> df.equals(pd.DataFrame({
    ...     'filename': ['file1.wav'], 
    ...     'start': [20.0], 
    ...     'end': [40.0], 
    ...     'label': [0], 
    ...     'score': [[0.6]]
    ... }))
    True
    >>> data = {
    ...     'filename': ['file1.wav'],
    ...     'start': [0.0],
    ...     'end': [60.0],
    ...     'score': [[
    ...         [0.8, 0.9, 0.7, 0.2, 0.1, 0.6, 0.9, 0.9, 0.2],
    ...         [0.7, 0.4, 0.6, 0.8, 0.6, 0.7, 0.8, 0.6, 0.1]
    ...     ]]
    ... }
    >>> df = convert_sequence_to_snapshot(data, 0.5, highest_score_only=True)
    >>> df = df.round(5) 
    >>> df.equals(pd.DataFrame({
    ...     'filename': ['file1.wav', 'file1.wav', 'file1.wav'], 
    ...     'start': [0.0, 20.0, 40.0], 
    ...     'end': [20.0, 40.0, 53.33333], 
    ...     'label': [0, 1, 0], 
    ...     'score': [[0.8, 0.9, 0.7], [0.8, 0.6, 0.7], [0.9, 0.9]]
    ... }))
    True
    """
    filtered_output = {'filename': [], 'start': [], 'end': [], 'label': [], 'score': []}
    
    for i in range(len(detections['filename'])):
        filename = detections['filename'][i]
        start = detections['start'][i]
        end = detections['end'][i]
        scores_list = detections['score'][i]
        
        # convert the score list into a numpy array for efficient computation
        scores = np.array(scores_list)
        # create mask where scores is above the threshold
        mask = scores > threshold

        if highest_score_only:
            # create mask where we keep the maximum between the classes
            mask2 = scores.max(axis=0, keepdims=1) == np.array(scores_list)
            # the final mask will be scores above the threshold and only the maximum score for that particular segment out of the classes
            mask = np.logical_and(mask, mask2)

        for label, score_list in enumerate(scores):
            # apply the mask to the score list for this particular class and get the index where the value is true
            filtered_indexes = np.where(mask[label] == True)[0]

            if filtered_indexes.size > 0:
                # grouping consecutive numbers
                for k, g in groupby(enumerate(filtered_indexes), key=lambda x: x[0] - x[1]):
                    group = list(map(itemgetter(1), g)) # gets the original index (without the position from enumerate)
                    start_time = start + group[0] / len(score_list) * (end - start) # here we are converting frames back into seconds.
                    end_time = start + (group[-1] + 1) / len(score_list) * (end - start)  # plus one because end time should be exclusive
                    filtered_output['filename'].append(filename)
                    filtered_output['start'].append(start_time)
                    filtered_output['end'].append(end_time)
                    filtered_output['label'].append(label)
                    filtered_output['score'].append(score_list[group].tolist())
    
    df = pd.DataFrame(filtered_output)
    
    return df.sort_values(by=['start'], ignore_index=True)

def filter_by_label(detecitons, labels):
    """
    Filters the input DataFrame by specified label(s).
    
    Args:
        detections: pandas DataFrame
            A DataFrame containing the results data.
        labels: list or integer 
            A list of labels to filter by.

    Returns:
        pandas.DataFrame: 
            A DataFrame containing only the detections with the specified labels.

    Example:

    >>> import pandas as pd
    >>> df = pd.DataFrame({
    ...     'filename': ['file1.wav', 'file2.wav', 'file3.wav'],
    ...     'start': [0.0, 20.0, 40.0],
    ...     'end': [20.0, 40.0, 60.0],
    ...     'label': [0, 1, 2],
    ...     'score': [0.6, 0.8, 0.7]
    ... })
    >>> filtered_df = filter_by_label(df, 1)
    >>> filtered_df = filtered_df.reset_index(drop=True)
    >>> filtered_df.equals(pd.DataFrame({
    ...     'filename': ['file2.wav'],
    ...     'start': [20.0],
    ...     'end': [40.0],
    ...     'label': [1],
    ...     'score': [0.8]
    ... }))
    True

    """
    if not isinstance(labels, list):
        labels = [labels]
    return detecitons[detecitons['label'].isin(labels)]

def merge_overlapping_detections(detections_df):
    """ Merge overlapping or adjacent detections with the same label.

        The score of the merged detection is computed as the average of the individual detection scores.

        Note: The detections are assumed to be sorted by start time in chronological order.

        Args:
            detections_df: pandas DataFrame
                Dataframe with detections. It should have the following columns:
                - 'filename': The name of the file containing the detection.
                - 'start': The start time of the detection in seconds.
                - 'end': The end time of the detection in seconds.
                - 'label': The label associated with the detection.
                - 'score': The score associated with the detection.
        
        Returns:
            merged: pandas DataFrame
                DataFrame with the merged detections.

        Example:
            Given a DataFrame with the following format:

            +----------+-------+-----+-------+-------+
            | filename | start | end | label | score |
            +----------+-------+-----+-------+-------+
            | file1    | 0     | 5   | 0     | 1     |
            +----------+-------+-----+-------+-------+
            | file1    | 3     | 7   | 0     | 2     |
            +----------+-------+-----+-------+-------+
            | file2    | 0     | 5   | 1     | 3     |
            +----------+-------+-----+-------+-------+

            The function would return:
            
            +----------+-------+-----+-------+-------+
            | filename | start | end | label | score |
            +----------+-------+-----+-------+-------+
            | file1    | 0     | 7   | 0     | 1.5   |
            +----------+-------+-----+-------+-------+
            | file2    | 0     | 5   | 1     | 3     |
            +----------+-------+-----+-------+-------+

        >>> import pandas as pd
        >>> detections_df = pd.DataFrame([
        ...     {'filename': 'file1', 'start': 0, 'end': 5, 'label': 0, 'score': 1},
        ...     {'filename': 'file1', 'start': 3, 'end': 7, 'label': 0, 'score': 2},
        ...     {'filename': 'file2', 'start': 0, 'end': 5, 'label': 1, 'score': 3}
        ... ])
        >>> merged = merge_overlapping_detections(detections_df)
        >>> merged.to_dict('records')
        [{'filename': 'file1', 'start': 0, 'end': 7, 'label': 0, 'score': 1.5}, {'filename': 'file2', 'start': 0, 'end': 5, 'label': 1, 'score': 3.0}]
    """
    detections = detections_df.to_dict('records')

    if len(detections) <= 1:
        return detections_df
    
    merged_detections = [detections[0]]

    for i in range(1,len(detections)):
        # detections do not overlap, nor are they adjacent nor they are from the same label
        if detections[i]['start'] > merged_detections[-1]['end'] or detections[i]['filename'] != merged_detections[-1]['filename'] or detections[i]['label'] != merged_detections[-1]['label']:
            merged_detections.append(detections[i])
        # detections overlap, or adjacent to one another
        else:
            # determine if the score is a list or a single number
            if isinstance(merged_detections[-1]['score'], list):
                overlap = merged_detections[-1]['end'] - detections[i]['start'] + 1 # amount of overlap

                # handle the scores
                merged_scores = merged_detections[-1]['score'][: -overlap]  # get the non-overlapping part from the first detection
                overlap_scores_merged = merged_detections[-1]['score'][-overlap:]  # get the overlapping part from the first detection
                overlap_scores_new = detections[i]['score'][:overlap]  # get the overlapping part from the second detection
                overlap_scores_avg = [(x + y) / 2 for x, y in zip(overlap_scores_merged, overlap_scores_new)]  # average the overlapping scores
                
                merged_scores += overlap_scores_avg  # add the averaged overlapping scores to the merged scores
                merged_scores += detections[i]['score'][overlap:]  # add the non-overlapping part from the second detection to the merged scores
            else:
                # if score is a single number, just average it as before
                merged_scores = (merged_detections[-1]['score'] + detections[i]['score']) / 2
            
            # create the new merged detection
            merged_detection = {
                'filename': detections[i]['filename'], 
                'start': merged_detections[-1]['start'], 
                'end': detections[i]['end'], 
                'label': detections[i]['label'], # add the label of the merged detection
                'score': merged_scores
            }

            merged_detections[-1] = merged_detection #replace

    return pd.DataFrame(merged_detections)
    
def merge_consecutive_detections(detections_df, step_size):
    # This implementation has several questions:

    # Consider if we really need this

    # 1) what happens when there are for instance, two consecutive detections for instance, from 0-3 and 1-4 and then one from 3-6? Does this create 2 detections or 1 detection? The current implementation creates 2
    # 2) See this: https://git-dev.cs.dal.ca/meridian/ketos/-/issues/18
    # 4) what if the step size is greater than the duration?
    """ Merges consecutive detections in the given dataframe.

        Consecutive detections are merged into a single detection event represented by the time interval start-end. 
        Consecutive detections are determined by the step_size parameter. The start time of the merged detection 
        will be the start time of the first consecutive detection. The end time of the merged detection will be
        adjusted to be 'step_size units after the start of the last consecutive detection.
        
        If the detections are not consecutive, each detection will have its end time adjusted to be 'step_size units after the start.
    
        See examples below.

        Args:
            detections_df: pandas DataFrame
                Dataframe with detections. It should have the following columns:
                - 'filename': The name of the file containing the detection.
                - 'start': The start time of the detection in seconds.
                - 'end': The end time of the detection in seconds.
                - 'label': The label associated with the detection.
                - 'score': The score associated with the detection.
            step_size: float
                The time interval (in seconds) between the starts of each continuous inputs.
                For example, a step=0.5 indicates that the first spectrogram starts at time 0.0s (from the beginning of the audio file), the second at 0.5s, etc.

        Returns:
            merged: pandas DataFrame
                DataFrame with the merged detections.

        Examples:

        >>> import pandas as pd
        >>> detections_df = pd.DataFrame({
        ...     'filename': ['file1', 'file1', 'file2', 'file2'],
        ...     'start': [0.0, 2.0, 0.0, 10.0],
        ...     'end': [3.0, 5.0, 3.0, 13.0],
        ...     'label': [1, 1, 1, 1],
        ...     'score': [0.8, 0.6, 0.9, 0.7]
        ... })
        >>> step_size = 2.0
        >>> merged = merge_consecutive_detections(detections_df, step_size)
        >>> merged
          filename  start   end  label  score
        0    file1    0.0   4.0      1    0.7
        1    file2    0.0   2.0      1    0.9
        2    file2   10.0  12.0      1    0.7
    """
    if len(detections_df) == 0:
        return detections_df
    
    if step_size < 0:
        raise ValueError("step_size must be non-negative")
    
    merged_detections = []
    for _, group in detections_df.groupby('filename'):
        group = group.to_dict('records') # transforming to dict for faster and easier looping

        merged_detection = {'filename': group[0]['filename'], 'start': group[0]['start'], 'end': group[0]['start'] + step_size, 'label': group[0]['label'], 'score': group[0]['score']}
        consecutives = 1 # start a counter of consecutive detections

        for i in range(1, len(group)):
            # detections are consecutive and have the same label
            if math.isclose(group[i-1]['start'] + step_size, group[i]['start']) and group[i-1]['label'] == group[i]['label']:
                consecutives += 1

                if isinstance(group[-1]['score'], list):
                    merged_detection['score'] = [sum(x) for x in zip(merged_detection['score'], group[i]['score'])]
                else:
                    merged_detection['score'] += group[i]['score']

                merged_detection['end'] = group[i]['start'] + step_size

            else:
                # finish the previous merged detection
                if isinstance(group[-1]['score'], list):
                    merged_detection['score'] = [score / consecutives for score in merged_detection['score']]
                else:
                    merged_detection['score'] /= consecutives
                merged_detections.append(merged_detection)

                merged_detection = {'filename': group[i]['filename'], 'start': group[i]['start'], 'end': group[i]['start'] + step_size, 'label': group[i]['label'], 'score': group[i]['score']}
                consecutives = 1

        # finish the last merged detection
        if isinstance(group[-1]['score'], list):
            merged_detection['score'] = [score / consecutives for score in merged_detection['score']]
        else:
            merged_detection['score'] /= consecutives
        merged_detections.append(merged_detection)
    
    return pd.DataFrame(merged_detections)