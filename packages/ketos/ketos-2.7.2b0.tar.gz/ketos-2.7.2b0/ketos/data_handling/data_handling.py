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

""" Data handling module within the ketos library

    This module provides utilities to load and handle data files.
"""
import numpy as np
import soundfile as sf
import datetime
import datetime_glob
import pandas as pd
import os
from ketos.audio.waveform import get_duration
from random import sample
from pathlib import Path

def parse_datetime(to_parse, fmt=None, replace_spaces='0'):
    """ Parse date-time data from string.
       
        Returns None if parsing fails.

        If the year is encoded with only two figures, it is parsed to 
        the most recent past year ending in those two figures. For 
        example, 45 would be parsed to 1945 (assuming that the program 
        is being executed in a year earlier than 2045).
        
        Args:
            to_parse: str
                String with date-time data to parse.
            fmt: str
                String defining the date-time format. 
                Example: %d_%m_%Y* would capture "14_3_1999.txt"
                See https://pypi.org/project/datetime-glob/ for a list of valid directives. 
                In addition to the directives allowed by the datetime-glob package, it is 
                also possible to specify %S.%ms for milliseconds. Note that the milliseconds
                (%ms) must follow the seconds (%S) separated by a period (.) or underscore (_) 
                and can only be followed by an asterisk (*) or nothing.            
            replace_spaces: str
                If string contains spaces, replaces them with this string

        Returns:
            datetime: datetime object

        Examples:
            >>> #This will parse dates in the day/month/year format,
            >>> #separated by '/'. It will also ignore any text after the year,
            >>> # (such as a file extension )
            >>>
            >>> from ketos.data_handling.data_handling import parse_datetime           
            >>> fmt = "%d/%m/%Y*"
            >>> result = parse_datetime("10/03/1942.txt", fmt)
            >>> result.year
            1942
            >>> result.month
            3
            >>> result.day
            10
            >>>
            >>> # Now with the time (hour:minute:second) separated from the date by an underscore
            >>> fmt = "%H:%M:%S_%d/%m/%Y*"
            >>> result = parse_datetime("15:43:03_10/03/1918.wav", fmt)
            >>> result.year
            1918
            >>> result.month
            3
            >>> result.day
            10
            >>> result.hour
            15
            >>> result.minute
            43
            >>> result.second
            3
    """
    # millisecond
    millisecond = False
    for sep in [".","_"]:
        if f'%S{sep}%ms' in fmt:
            millisecond = True
            fmt = fmt.replace(f'%S{sep}%ms', '%S*')

    # replace spaces
    to_parse = to_parse.replace(' ', replace_spaces)
    
    if fmt is not None:
        matcher = datetime_glob.Matcher(pattern=fmt)
        match = matcher.match(path=to_parse)
        if match is None:
            return None
        else:
            dt = match.as_datetime()
            if dt > datetime.datetime.now() and "%y" in fmt: dt = dt.replace(year=dt.year-100)

            if millisecond:
                dt_str = dt.strftime(fmt)
                dt_str = dt_str.replace('*','')
                i = to_parse.rfind(dt_str) + len(dt_str) + 1
                ms_str = to_parse[i:i+3]
                ms = int(ms_str)
                dt += datetime.timedelta(microseconds=1e3*ms)

            return dt

    return None

def find_files(path, substr, return_path=True, search_subdirs=False, search_path=False):
    """Find all files in the specified directory containing the specified substring in their file name or path.

    Args:
        path: str or Path
            Directory path.
        substr: str
            Substring contained in file name or path.
        return_path: bool
            If True, return the path to each file, relative to the top directory. 
            If False, only return the filenames.
        search_subdirs: bool
            If True, search all subdirectories.
        search_path: bool
            If True, search for substring occurrence in the relative path rather than just the filename.

    Returns:
        files: list (str)
            Alphabetically sorted list of file names or paths.
    """
    path = Path(path)
    if isinstance(substr, str):
        substr = [substr]
    
    if search_subdirs:
        files = path.rglob('*')
    else:
        files = path.glob('*')

    matching_files = []
    
    for file in files:
        relative_path = file.relative_to(path)
        search_target = str(relative_path) if search_path else file.name
        if any(ss in search_target for ss in substr):
            matching_files.append(str(relative_path) if return_path else file.name)

    return sorted(matching_files)


def find_audio_files(path, extensions=None, return_path=True, search_subdirs=False, search_path=False):
    """ Find all audio files in the specified directory with specified extensions.

        Args:
            path: str
                Directory path.
            extensions: list (str)
                List of file extensions to search for (e.g., ['.wav', '.mp3', '.flac']).
                If None, use a default list of common audio file extensions.
            return_path: bool
                If True, path to each file, relative to the top directory.
                If False, only return the filenames.
            search_subdirs: bool
                If True, search all subdirectories.
            search_path: bool
                Search for substring occurrence in relative path rather than just the filename.

        Returns:
            : list (str)
                Alphabetically sorted list of file names or paths.

        Examples:
            >>> from ketos.data_handling.data_handling import find_audio_files
            >>>
            >>> find_audio_files(path="ketos/tests/assets", extensions=['.wav', '.mp3'], return_path=False)
            ['2min.wav', 'empty.wav', 'grunt1.wav', 'super_short_1.wav', 'super_short_2.wav']

    """
    # Default list of common audio file extensions
    if extensions is None:
        extensions = ['.wav', '.mp3', '.flac', '.aiff', '.ogg', '.wma', '.m4a']

    # Ensure all extensions are lowercase for consistency
    extensions = [ext.lower() for ext in extensions]

    # Modify the find_files call to search for any of the specified extensions
    return find_files(path, substr=extensions, return_path=return_path,
                      search_subdirs=search_subdirs, search_path=search_path)

def file_duration_table(path, num=None, exclude_subdir=None):
    """ Create file duration table.

        Args:
            path: str
                Path to folder with audio files (\*.wav)
            num: int
                Randomly sample a number of files
            exclude_subdir: str
                Exclude subdir from the search 

        Returns:
            df: pandas DataFrame
                File duration table. Columns: filename, duration, (datetime)
    """
    paths = find_files(path=path, substr=['.wav', '.WAV', '.flac', '.FLAC'], search_subdirs=True, return_path=True)
    
    if exclude_subdir is not None:
        paths = [path for path in paths if exclude_subdir not in path]

    if num is not None:
        paths = sample(paths, num)

    durations = get_duration([os.path.join(path,p) for p in paths])
    df = pd.DataFrame({'filename':paths, 'duration':durations})
    return df

def to1hot(value: int | float | np.ndarray, n_classes: int = -1) -> np.array:
    """Converts the binary label to one hot format

            Args:
                value
                    The the label to be converted.
                n_classes
                    The number of classes. If set to -1, the number of classes 
                    will be inferred from the input values as one greater than 
                    the largest class value in the input.
                                
            Returns:
                one_hot:numpy array (dtype=float64)
                    A len(value) by n_classes array containg the one hot encoding
                    for the given value(s).

            Example:
                >>> from ketos.data_handling.data_handling import to1hot
                >>>
                >>> # An example with two possible labels (0 or 1)
                >>> values = np.array([0,1])
                >>> to1hot(values,n_classes=2)
                array([[1., 0.],
                       [0., 1.]])
                >>>
                >>> # The same example with 4 possible labels (0,1,2 or 3)
                >>> values = np.array([0,1])
                >>> to1hot(values,n_classes=4)
                array([[1., 0., 0., 0.],
                       [0., 1., 0., 0.]])
                >>>
                >>> to1hot(1, n_classes=3)
                array([0., 1., 0.])

                >>> values = np.array([0, 1, 2, 3])
                >>> to1hot(values, n_classes=-1)
                array([[1., 0., 0., 0.],
                       [0., 1., 0., 0.],
                       [0., 0., 1., 0.],
                       [0., 0., 0., 1.]])
     """
    value = np.int64(value)
    if n_classes == -1:
        n_classes = np.max(value) + 1
    one_hot = np.eye(n_classes)[value]
    return one_hot

def from1hot(value):
    """Converts the one hot label to binary format

            Args:
                value: scalar or numpy.array | int or float
                    The  label to be converted.
            
            Returns:
                output: int or numpy array (dtype=int64)
                    An int representing the category if 'value' has 1 dimension or an
                    array of m ints if values is an n by m array.

            Example:
                >>> from ketos.data_handling.data_handling import from1hot
                >>>
                >>> from1hot(np.array([0,0,0,1,0]))
                3
                >>> from1hot(np.array([[0,0,0,1,0],
                ...   [0,1,0,0,0]]))
                array([3, 1])

     """

    if value.ndim > 1:
        output = np.apply_along_axis(arr=value, axis=1, func1d=np.argmax)
        output.dtype = np.int64
    else:
        output = np.argmax(value)

    return output
