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

""" Data feeding module within the ketos library

    This module provides utilities to load data and feed it to models.

    Contents:
        BatchGenerator class
        
        TrainiDataProvider class
"""
import warnings
import numpy as np
import pandas as pd
from sklearn.utils import shuffle



class BatchGenerator():
    """ Creates batches to be fed to a model

        Instances of this class are python generators. They will load one batch at 
        a time from a HDF5 database, which is particularly useful when working with 
        larger than memory datasets.
        
        It is also possible to load the entire data set into memory and provide it 
        to the BatchGenerator via the arguments x and y. This can be convenient when 
        working with smaller data sets.

        Yields:
        (X,Y) or (ids,X,Y) if 'return_batch_ids' is True.

            X is a batch of data in the form of an np.array of shape (batch_size,mx,nx) where 
            mx,nx are the shape of one instance of X in the database. The number
            of dimensions in addition to 'batch_size' will not necessarily be 2, but correspond to
            the instance shape (1 for 1d instances, 3 for 3d, etc).

            It is also possible to load multiple data objects per instance by specifying multiple x_field 
            values, e.g., 'x_field=['spectrogram', 'waveform']'. In such cases, the return argument X is a 
            np.array with shape (batch_size,) and each element is a np.void array with length equal to the 
            number of x fields. Each element in this array is a np.array and can be accessed either through 
            use of integer indices or the x_field names, e.g., the first spectrogram in the batch can be 
            accessed as X[0][0] or X[0]['spectrogram'].

            Similarly, Y is an np.array of shape(batch_size) with the corresponding labels.
            Each item in the array is a named array of shape=(n_fields), where n_field is the number of fields
            specified in the 'y_field' argument. For instance, if 'y_field'=['label', 'start', 'end'], you can access
            the first label with Y[0]['label'].
            Notice that even if y_field==['label'], you would still use the Y[0]['label'] syntax.

            If y_field=None, Y will return None. This can be usefull if you are creating the labels dinamically or
            or if usign the BatchGeneratot for inference.

            Important note: The above remarks regarding the shapes of X and Y assume that the output 
            transform function `output_transform_func` only modifies the contents and not the shapes 
            of X and Y, which may not always be the case.
        
        Args:
            batch_size: int
                The number of instances in each batch. The last batch of an epoch might 
                have fewer examples, depending on the number of instances in the hdf5_table.
                If the batch size is greater than the number of instances available, batch_size will 
                be set to the number of instances. and a warning will be issued
            data_table: pytables table (instance of table.Table()) 
                The HDF5 table containing the data
            annot_table: pytables table (instance of table.Table()) 
                A separate table for the annotations(labels), in case they are not included as fields in the data_table.
                This table must have a 'data_index' field, which corresponds to the the index (row number) of the data instance in the data_tables.
                Usually, a separete table will be used when the data is strongly annotated (i.e.: possibily more than one annotation per data instance).
                When there is only one annotation for each data instance, it's recommended that annotations are included in the data_table for performance gains.
            x: numpy array
                Array containing the data images.
            y: numpy array
                Array containing the data labels. 
                This array is expected to have a one-to-one correspondence to the x array (i.e.: y[0] is expected to have the label for x[0], y[1] for x[1], etc).
                If there are multiple labels for each data instance in x, use a data_table and an annot_table instead.
            select_indices: list of ints
                Indices of those instances that will retrieved from the HDF5 table by the 
                BatchGenerator. By default all instances are retrieved.
            output_transform_func: function
                A function to be applied to the batch, transforming the instances. Must accept 
                'X' and 'Y' and, after processing, also return  'X' and 'Y' in a tuple.
            x_field: str
                The name of the column containing the X data in the hdf5_table
            y_field: str
                The name of the column containing the Y labels in the hdf5_table. Can be None.
            shuffle: bool
                If True, instances are selected randomly (without replacement). If False, 
                instances are selected in the order the appear in the database
            refresh_on_epoch_end: bool
                If True, and shuffle is also True, resampling is performed at the end of 
                each epoch resulting in different batches for every epoch. If False, the 
                same batches are used in all epochs.
                Has no effect if shuffle is False.
            return_batch_ids: bool
                If False, each batch will consist of X and Y. If True, the instance indices 
                (as they are in the hdf5_table) will be included ((ids, X, Y)).
            filter: str
                A valid PyTables query. If provided, the Batch Generator will query the hdf5
                database before defining the batches and only the matching records will be used.
                Only relevant when data is passed through the hdf5_table argument. If both 'filter'
                and 'indices' are passed, 'indices' is ignored.
            n_extend: int
                Extend every batch by including the last n_extend samples from 
                the previous batch and the first n_extend samples from the following batch.
                The first batch is only extended at the end, while the last batch is only 
                extended at the beginning. The default value is zero, i.e., no extension.  

        Attr:
            data: pytables table (instance of table.Table()) 
                The HDF5 table containing the data
            n_instances: int
                The number of intances (rows) in the hdf5_table
            n_batches: int
                The number of batches of size 'batch_size' for each epoch
            entry_indices:list of ints
                A list of all intance indices, in the order used to generate batches for this epoch
            batch_indices: list of tuples (int,int)
                A list of (start,end) indices for each batch. These indices refer to the 'entry_indices' attribute.
            batch_count: int
                The current batch within the epoch. This will be the batch yielded on the next call to 'next()'.
            from_memory: bool
                True if the data are loaded from memory rather than an HDF5 table.

        Examples:
            >>> from tables import open_file
            >>> h5 = open_file("ketos/tests/assets/11x_same_spec.h5", 'r') # create the database handle  
            >>> data_table = h5.get_node("/group_1/table_data")
            >>> annot_table = h5.get_node("/group_1/table_annot")
            >>> #Create a BatchGenerator from a data_table and separate annotations in a anot_table
            >>> train_generator = BatchGenerator(data_table=data_table, annot_table=annot_table, batch_size=3, x_field='data', return_batch_ids=True) #create a batch generator 
            >>> #Run 2 epochs. 
            >>> n_epochs = 2    
            >>> for e in range(n_epochs):
            ...    for batch_num in range(train_generator.n_batches):
            ...        ids, batch_X, batch_Y = next(train_generator)
            ...        print("epoch:{0}, batch {1} | instance ids:{2}, X batch shape: {3} labels for instance {4}: {5}".format(e, batch_num, ids, batch_X.shape, ids[0], batch_Y[0]))
            epoch:0, batch 0 | instance ids:[0, 1, 2], X batch shape: (3, 12, 12) labels for instance 0: [2, 3]
            epoch:0, batch 1 | instance ids:[3, 4, 5], X batch shape: (3, 12, 12) labels for instance 3: [2, 3]
            epoch:0, batch 2 | instance ids:[6, 7, 8, 9, 10], X batch shape: (5, 12, 12) labels for instance 6: [2, 3]
            epoch:1, batch 0 | instance ids:[0, 1, 2], X batch shape: (3, 12, 12) labels for instance 0: [2, 3]
            epoch:1, batch 1 | instance ids:[3, 4, 5], X batch shape: (3, 12, 12) labels for instance 3: [2, 3]
            epoch:1, batch 2 | instance ids:[6, 7, 8, 9, 10], X batch shape: (5, 12, 12) labels for instance 6: [2, 3]
            >>> h5.close() #close the database handle.
            >>> # Creating a Batch Generator from a data tables that includes annotations
            >>> h5 = open_file("ketos/tests/assets/mini_narw.h5", 'r') # create the database handle  
            >>> data_table = h5.get_node("/train/data")
            >>> #Applying a custom function to the batch
            >>> #Takes the mean of each instance in X; leaves Y untouched
            >>> def apply_to_batch(X,Y):
            ...    X = np.mean(X, axis=(1,2)) #since X is a 3d array
            ...    return (X,Y)
            >>> train_generator = BatchGenerator(data_table=data_table, batch_size=3, return_batch_ids=False, output_transform_func=apply_to_batch) 
            >>> X,Y = next(train_generator)                
            >>> #Now each X instance is one single number, instead of a 2d array
            >>> #A batch of size 3 is an array of the 3 means
            >>> X.shape
            (3,)
            >>> #Here is how one X instance looks like
            >>> X[0]
            -37.247124
            >>> #Y is the same as before 
            >>> Y.shape
            (3,)
            >>> h5.close()
    """
    def __init__(self, batch_size, data_table=None, annot_table=None, x=None, y=None, 
                    select_indices=None, output_transform_func=None, x_field='data', y_field='label',
                    shuffle=False, refresh_on_epoch_end=False, return_batch_ids=False, filter=None, n_extend=0):

        self.from_memory = x is not None and y is not None
        self.filter = filter
        self.unique_labels = None
        
        if self.from_memory:
            self.x = x
            self.y = y

            if select_indices is None:
                self.select_indices = np.arange(len(self.x), dtype=int) 
            else:
                self.select_indices = select_indices
            self.n_instances = len(self.select_indices)
        
        else:
            assert (data_table is not None), 'data_table or x and y must be specified'

            self.data = data_table
            self.annot_table = annot_table
            self.x_field = x_field

            if y_field is not None:
                self.y_field = [y_field] if type(y_field) is not list else y_field

            if select_indices is None:
                self.n_instances = self.data.nrows
                self.select_indices = self.data.col('id')
            else:
                self.n_instances = len(select_indices)
                self.select_indices = select_indices

            if self.filter is not None:
                self.id_row_index = self.data.get_where_list(self.filter)
                self.select_indices = self.data[self.id_row_index]['id']
                self.n_instances = len(self.select_indices)

        self.batch_size = batch_size
        if self.batch_size > self.n_instances:
            warnings.warn("The batch size is greater than the number of instances available. Setting batch_size to n_instances.")
            self.batch_size = self.n_instances

        self.shuffle = shuffle
        self.output_transform_func = output_transform_func
        self.batch_count = 0
        self.refresh_on_epoch_end = refresh_on_epoch_end
        self.return_batch_ids = return_batch_ids

        self.n_batches = int(self.n_instances // self.batch_size)

        self.__update_indices__()
        self.__create_batches__(n_extend)


    def __update_indices__(self, indices=None):
        """ Updates the indices used to divide the instances into batches.

            A list of indices is kept in the self.data_indices attribute.
            The order of the indices determines which instances will be placed in each batch.
            If the self.shuffle is True, the indices are randomly reorganized, resulting in 
            batches with randomly selected instances.
        """
        if indices is None:
            self.data_indices = self.select_indices.copy()
            if self.shuffle:
                np.random.shuffle(self.data_indices)        
        else:
            self.data_indices = indices

    def __create_batches__(self, n_ext=0):
        """ Prepare batches.

            Divides the indices into batches of self.batch_size, based on the list generated 
            by `update_indices()`.

            Args:
                n_ext: int
                    Extend every batch by including the last n_extend samples from 
                    the previous batch and the first n_extend samples from the following batch.
                    The first batch is only extended at the end, while the last batch is only 
                    extended at the beginning. The default value is zero, i.e., no extension.  

            Returns:
                list_of_indices: list of tuples
                    A list of tuple, each containing two integer values: the start and end of the batch. 
                    These positions refer to the list stored in self.entry_indices.                
        
        """
        ids = self.data_indices  # for brevity

        n_complete_batches = int( self.n_instances // self.batch_size) # number of batches that can accomodate self.batch_size intances
        extra_instances = self.n_instances % self.batch_size

        if n_complete_batches == 0: 
            list_of_indices = [list(ids)]
        else:
            n = self.batch_size
            list_of_indices = [list(ids[max(0,i*n-n_ext):min(n*n_complete_batches,(i+1)*n+n_ext)]) for i in range(n_complete_batches)]
            if extra_instances > 0:
                extra_instance_ids = list(ids[-extra_instances:])
                list_of_indices[-1] = list_of_indices[-1] + extra_instance_ids

        if self.from_memory:
            data_indices = list_of_indices
            annot_indices = list_of_indices
        
        else:
            data_indices = list_of_indices
            
            if self.annot_table:
                index = np.array([(row['data_index'], annot_idx) for annot_idx,row in \
                    enumerate(self.annot_table.iterrows()) if row['data_index'] in self.select_indices])

                if len(index) > 0:
                    annot_indices = [[index[index[:,0]==data_idx,1] for data_idx in batch] for batch in list_of_indices] 
                    annot_indices = [np.concatenate(batch) for batch in annot_indices]
    
                else:
                    annot_indices = [None for _ in data_indices]

            else:
                annot_indices = None

        self.batch_indices_data = data_indices
        self.batch_indices_annot = annot_indices

    def reset(self, indices=None):
        """ Reset the batch generator.

            Resets the batch index counter and reshuffles the sample indices 
            if shuffle was set to True.

            Args:
                indices: array
                    Manually specify the sequence of indices that should be used 
                    after reset.
        """
        if (self.refresh_on_epoch_end and self.batch_count > 0) or indices is not None:
            self.__update_indices__(indices)
            self.__create_batches__()

        self.batch_count = 0

    def get_indices(self):
        ''' Get the indice sequence used for sampling the data table

            Returns:
                : array
                    Indices
        '''
        return self.data_indices

    def set_return_batch_ids(self, v):
        ''' Change the behaviour of the generator between returning
            only X,Y or id,X,Y

            Args:
                v: bool
                    Whether to return id in addition to X,Y
        '''
        self.return_batch_ids = v

    def set_shuffle(self, v):
        ''' Change the behaviour of the generator between shuffling or not 
            shuffling the indices.

            Args:
                v: bool
                    Whether to return shuffle the indices
        '''
        self.shuffle = v

    def get_samples(self, indices, annot_indices=None):
        """ Get data samples for specified indices

            Args:
                indices: list of ints
                    Row indices of the samples in the data table
                annot_indices: list of ints
                    Row indices of the matching samples in the annotation table, if applicable.

            Returns: 
                : tuple
                    A batch of instances (X,Y) 
        """
        if self.from_memory:
            X = np.take(self.x, indices, axis=0)
            if self.y is not None:
                Y = np.take(self.y, indices, axis=0)
            else:
                Y = None
        else:
            X = self.data[indices][self.x_field]

            if self.y_field is None:
                Y = None
            elif not self.annot_table:
                Y = self.data[indices][self.y_field]  #['label']

                # if there is only 1 y-field, convert the ndarray to a normal array
                if len(self.y_field) == 1:
                    Y = Y[self.y_field[0]]

            else:              
                if annot_indices is None:
                    Y = [None for _ in X]

                else:
                    data_indices = self.annot_table.col('data_index')[annot_indices]
                    Y = self.annot_table[annot_indices][self.y_field]

                    # count how many times each data index occurs in the annotation table
                    index_mul = [np.sum(data_indices==i) for i in indices]

                    # group the labels according to thir data index
                    sections = np.cumsum(index_mul)[:-1]
                    Y = np.split(Y, sections)
                    
                    # if there is only 1 y-field, convert the ndarray to a normal array
                    if len(self.y_field) == 1:
                        Y = [list(y[self.y_field[0]]) for y in Y]
                

        if self.output_transform_func is not None:
            X,Y = self.output_transform_func(X,Y)

        return (X, Y)

    def __iter__(self):
        return self

    def __next__(self):
        """         
            Return: tuple
            A batch of instances (X,Y) or, if 'returns_batch_ids" is True, a batch of instances accompanied by their indices (ids, X, Y) 
        """
        data_row_index = self.batch_indices_data[self.batch_count]
        
        if not self.from_memory and self.annot_table:
            annot_row_index = self.batch_indices_annot[self.batch_count]
        else:
            annot_row_index = None

        self.batch_count += 1
        if self.batch_count > (self.n_batches - 1):
            self.reset()

        (X,Y) = self.get_samples(indices=data_row_index, annot_indices=annot_row_index)

        if self.return_batch_ids:
            return (data_row_index,X,Y)
        else:
            return (X, Y)


class JointBatchGen():
    """ Join two or more batch generators.

        A joint batch generator is composed by multiple BatchGenerator objects.
        It offers a flexible way of composing custom batches for training neural networks.
        Each batch is composed by joining the batches of all generators in the 'batch_generators' list.

        In order to be able to combine batch generators in this manner, the batch generators must 
        yield data batches (X,Y) with the same format. Furthermore, the first dimension must be 
        the batch size. In the case of multimodal generators, the second dimension must be the 
        number of modes.

        For example, if the generator is returning a waveform and a spectrogram, and the batch size 
        was set to 32, the JointBatchGen expects X to have length 32 and every element in X to have 
        length 2 (corresponding to the two modalities, waveform and spectrogram).

        An assertion is made at initialization to check that all batch generators yield data with 
        consistent formats. If the assertion fails, an error is thrown.

        Args:
            batch_generators: list of BatchGenerator objects
                A list of 2 or more BatchGenerator instances.
            n_batches: str or int (default:'min')
                The number of batches for the joint generator. It can be an integer number, 'min',
                which will use the lowest n_batches among the batch generators, or 'max, which will 
                use the highest value.
            shuffle_batch:bool (default:False)
                If True, shuffle the joint batch before returning it. Note that this only concerns the 
                joint batches and is independent of wheter the joined generators shuffle or not.
            reset_generators:bool (default:False)
                If True, reset the current batch counter of each generator whenever the joint generator 
                reaches the n_batches value. This evokes the end-of-epoch behaviour for each batch generator 
                (i.e.: if a  batch generator was created with 'duffle_on_epoch_end=True', then it will 
                shuffle at this time, even if that generator's batch counter is not yet at the maximum).
            return_batch_ids: bool
                If False, each batch will consist of X and Y. If True, the generator index and the instance 
                indices (as they are in the hdf5_table) will be included ((ids, X, Y)). Default is False.
            output_transform_func: function
                A function to be applied to the joint batch, transforming the instances. Must accept 
                'X' and 'Y' and, after processing, also return  'X' and 'Y' in a tuple. 

        Example:
            >>> from tables import open_file
            >>> h5 = open_file("ketos/tests/assets/multimodal.h5", 'r') # create the database handle  
            >>> tbl_pos = h5.get_node("/train/pos/data") #table with positive samples
            >>> tbl_neg = h5.get_node("/train/neg/data") #table with negative samples
            >>> #Create batch generators for multi-modal data (waveform, spectrogram)
            >>> generator_pos = BatchGenerator(data_table=tbl_pos, batch_size=2, x_field=['waveform','spectrogram']) 
            >>> generator_neg = BatchGenerator(data_table=tbl_neg, batch_size=3, x_field=['waveform','spectrogram']) 
            >>> #Join the generators
            >>> generator = JointBatchGen([generator_pos, generator_neg])
            >>> #Loading the first batch, we note that the joint generator has a batch size of 2+3=5
            >>> #and the waveforms and spectrograms have shapes (3000,) and (129,94), respectively.
            >>> X, Y = next(generator)
            >>> print(len(X), len(X[0]), X[0][0].shape, X[0][1].shape)
            5 2 (3000,) (94, 129)
            >>> h5.close() #close the database handle.
    """
    def __init__(self, batch_generators, n_batches="min", shuffle_batch=False, reset_generators=False, 
                    return_batch_ids=False, output_transform_func=None):
        self.batch_generators = batch_generators
        self.reset_generators = reset_generators
        self.shuffle_batch = shuffle_batch
        self.return_batch_ids = return_batch_ids
        self.output_transform_func = output_transform_func

        assert n_batches in ("min", "max") or isinstance(n_batches, int), "n_batches must be 'min', 'max' or an integer"
        if n_batches == "min":
            self.n_batches = min([gen.n_batches for gen in self.batch_generators]) 
        elif n_batches == "max":
            self.n_batches = max([gen.n_batches for gen in self.batch_generators]) 
        else:
            self.n_batches = n_batches
        
        self.batch_count = 0

        # overwrite return_batch_ids attribute of individual generators,
        # determine batch size, and check if any of the generators are 
        # loading annotations from a separate annotation table.
        self.batch_size = 0        
        for generator in self.batch_generators: 
            generator.set_return_batch_ids(True)
            self.batch_size += generator.batch_size

        # check that the batch generators return consistent data types
        x_sizes = []
        y_sizes = []
        for generator in self.batch_generators:
            i,x,y = next(generator)
            x_sizes.append(len(x[0]) if isinstance(x[0], (np.void, list, tuple)) else 0)
            y_sizes.append(len(y[0]) if isinstance(y[0], (np.void, list, tuple)) else 0)
            generator.reset()

        assert np.all(np.array(x_sizes)==x_sizes[0]), 'Attempt to join batch generators with different X '\
            'output formats. Only batch generators with the same X and Y format may be joined'

        self.xsiz = x_sizes[0]
        self.ysiz = y_sizes[0]

    def __iter__(self):
        return self

    def __next__(self):

        X = []
        Y = []
        ids = []
        for gen_id, gen in enumerate(self.batch_generators):
            i,x,y = next(gen)
            i = np.column_stack((gen_id * np.ones(len(i)),i))
            i = i.astype(int)
            ids.append(i)

            if self.xsiz == 0:
                X.append(x)            
            else:
                X += [e for e in x]
            if self.ysiz == 0:
                Y.append(y)            
            else:
                Y += [e for e in y]

        if self.xsiz == 0:
            X = np.vstack(X)

        if self.ysiz == 0:
            Y = np.concatenate(Y)

        ids = np.vstack(ids)

        siz = len(X)

        if self.shuffle_batch == True:
            indices = np.arange(siz)
            np.random.shuffle(indices)
            if self.xsiz == 0:
                X = X[indices]
            else:
                X = [X[i] for i in indices]

            if self.ysiz == 0:
                Y = Y[indices]
            else:
                Y = [Y[i] for i in indices]

            if self.return_batch_ids:
                ids = ids[indices]

        self.batch_count += 1
        if self.batch_count > (self.n_batches - 1):
            self.batch_count = 0
            if self.reset_generators ==  True:
                for gen in self.batch_generators:
                    gen.reset()

        if self.output_transform_func is not None:
            X,Y = self.output_transform_func(X,Y)

        if self.return_batch_ids:
            return (ids,X,Y)
        else:                                                
            return (X,Y)

    def reset(self, indices=None):
        """ Resets the individual batch generators.

            Args:
                indices: array
                    Manually specify the sequence of indices that should be used 
                    after reset.
        """
        if indices is None:
            indices = [None for _ in self.batch_generators]
        else:
            assert isinstance(indices, list) and len(indices) == len(self.batch_generators),\
                "the length of 'indices' must match the number of batch generators."

        for idx,gen in zip(indices, self.batch_generators):
            gen.reset(indices=idx)

        self.batch_count = 0

    def get_indices(self):
        ''' Get the indice sequence used for sampling the data tables

            Returns:
                : array
                    Indices
        '''
        return [g.get_indices() for g in self.batch_generators]

    def set_return_batch_ids(self, v):
        ''' Change the behaviour of the generator between returning
            only X,Y or id,X,Y

            Args:
                v: bool
                    Whether to return id in addition to X,Y
        '''
        self.return_batch_ids = v
        for g in self.batch_generators:
            g.set_return_batch_ids(v)

    def set_shuffle(self, v):
        ''' Change the behaviour of the generator between shuffling or not 
            shuffling the indices.

            Args:
                v: bool
                    Whether to return shuffle the indices
        '''
        for g in self.batch_generators:
            g.set_shuffle(v)


class MultiModalBatchGen():
    """ Join two or more batch generators.

        A multi-modal batch generator is composed of multiple BatchGenerator objects.

        It is intended for use with multi-modal models, i.e., models that integrate several 
        data representations (e.g. waveform and spectrogram). In particular, the multi-modal 
        batch generator provides handy way to load data stored in separate tables.

        OBS: While the data may be stored in separate tables, the sample sequence must be 
        identical across tables and the tables must of course contain the same number of 
        entries.

        Each batch is composed by collecting batches from the individual generators to form a 
        a nested list, where the first dimension is the batch size and the second dimension 
        is the number of modes. (This ordering is chosen to be consistent with the conventions 
        used in the `BatchGenerator` and `JointBatchGen` classes.)

        An assertion is made at initialization to check that the batch generators are loading 
        data from tables with consistent lengths. If the assertion fails, an error is thrown.

        TODO: Add example

        Args:
            batch_generators: list of BatchGenerator objects
                A list of 2 or more BatchGenerator instances.
            batch_size: int
                The number of instances in each batch. 
            shuffle: bool
                If True, instances are selected randomly (without replacement). If False, 
                instances are selected in the order the appear in the database
            refresh_on_epoch_end: bool
                If True, and shuffle is also True, resampling is performed at the end of 
                each epoch resulting in different batches for every epoch. If False, the 
                same batches are used in all epochs.
                Has no effect if shuffle is False.
            return_batch_ids: bool
                If False, each batch will consist of X and Y. If True, the generator index and the instance 
                indices (as they are in the hdf5_table) will be included ((ids, X, Y)). Default is False.
            output_transform_func: function
                A function to be applied to the combined batch, transforming the instances. Must accept 
                'X' and 'Y' and, after processing, also return  'X' and 'Y' in a tuple. 
    """
    def __init__(self, batch_generators, batch_size=None, shuffle=False, refresh_on_epoch_end=False, 
        return_batch_ids=False, output_transform_func=None):
        
        self.batch_generators = batch_generators
        self.return_batch_ids = return_batch_ids
        self.refresh_on_epoch_end = refresh_on_epoch_end
        self.output_transform_func = output_transform_func
        self.batch_count = 0

        # overwrite attributes of individual generators
        for generator in self.batch_generators: 
            if batch_size is not None:
                generator.batch_size = batch_size
    
            generator.set_return_batch_ids(True)
            generator.set_shuffle(shuffle)
            
            assert generator.n_batches == self.batch_generators[0].n_batches, "All batch generators must have the same number of batches"
            assert generator.batch_size == self.batch_generators[0].batch_size, "All batch generators must have the same batch size" 

        # number of batches and batch size
        self.n_batches = self.batch_generators[0].n_batches
        self.batch_size = self.batch_generators[0].batch_size

        # update indices and create batches
        self.reset()

    def __iter__(self):
        return self

    def __next__(self):
        """ Get the next batch """
        self.batch_count += 1

        # collect the outputs of the individual batch generators
        X, Y = [], []
        for generator in self.batch_generators:
            ids,x,y = next(generator)
            X.append(x)
            Y.append(y)

        # invert ordering: gen,batch -> batch,gen 
        X = [[x[i] for x in X] for i in range(len(X[0]))]
        Y = [[y[i] for y in Y] for i in range(len(Y[0]))]

        if self.output_transform_func is not None:
            X,Y = self.output_transform_func(X,Y)

        if self.return_batch_ids:
            return (ids,X,Y)
        else:                                                
            return (X,Y)

    def reset(self, indices=None):
        """ Reset the batch generator.

            Resets the batch index counter and reshuffles the sample indices 
            if shuffle was set to True.

            Args:
                indices: array
                    Manually specify the sequence of indices that should be used 
                    after reset.
        """
        g0 = self.batch_generators[0]
        g0.reset(indices=indices)
        for generator in self.batch_generators: 
            generator.reset(indices=g0.get_indices())

        self.batch_count = 0

    def get_indices(self):
        ''' Get the indice sequence used for sampling the data table

            Returns:
                : array
                    Indices
        '''
        return self.batch_generators[0].get_indices()

    def set_return_batch_ids(self, v):
        ''' Change the behaviour of the generator between returning
            only X,Y or id,X,Y

            Args:
                v: bool
                    Whether to return id in addition to X,Y
        '''
        self.return_batch_ids = v
        for g in self.batch_generators:
            g.set_return_batch_ids(v)

    def set_shuffle(self, v):
        ''' Change the behaviour of the generator between shuffling or not 
            shuffling the indices.

            Args:
                v: bool
                    Whether to return shuffle the indices
        '''
        for g in self.batch_generators:
            g.set_shuffle(v)
