import tables as tb
import numpy as np

def generate_table_description(
    data_sample: np.ndarray,
    representation_name: str = 'representation_field'
) -> tb.IsDescription:
    """
    Returns a PyTables table description class with the shape inferred from
    a given data sample.

    Args:
        data_sample: numpy.ndarray
            A sample numpy array from which the shape of the `data` field will be inferred.
        representation_name: str 
            Name of the data field in the table (default: 'representation_field').

    Returns:
        tables.IsDescription
            A class representing the table description with the following fields:
            - `filename`: A string field to store the name of the file associated with the data.
            - `start`: A float field to store the start time (or other temporal reference) of the data relative the to the file.
            - `id`: An unsigned integer field to store a unique identifier for the data entry.
            - `label`: An unsigned 8-bit integer field to store a label or category for the data.
            - representation_name: A float32 array field with the shape inferred from `data_sample`, to store the actual data.
    
    Examples:
        >>> sample = np.random.rand(128, 256)
        >>> description = generate_table_description(sample)
        >>> issubclass(description, tb.IsDescription)
        True
    """
    if data_sample.size == 0:
        raise ValueError("The input data sample is empty. A non-empty array is required.")
    
    item_shape = data_sample.shape
    
    fields = {
        "filename": tb.StringCol(128),
        "start": tb.Float32Col(),
        "id": tb.UInt32Col(),
        "label": tb.UInt8Col(),
        representation_name: tb.Float32Col(shape=item_shape)
    }

    # Dynamically create a new IsDescription class
    return type("RepresentationTable", (tb.IsDescription,), fields)


def insert_representation_data(
    table: tb.Table, 
    filename: str, 
    start: float, 
    label: int, 
    representation_data: np.ndarray,
    representation_name: str = "representation_field"
) -> None:
    """
    Inserts a single row of representation data (e.g., waveform or spectrogram) 
    into the specified PyTables table.

    Args:
        table: tables.Table
            The PyTables table where the data will be inserted.
        filename: str
            The filename associated with the representation data.
        start: int or float
            The start time (or other temporal reference) of the data relative the to the file.
        label: int
            The label (as an integer) for the representation data.
        representation_data : numpy.ndarray
            The representation data as a numpy array (1D for waveforms or 2D for spectrograms).
        representation_field: str
            The field name of the representation in the table (default: "representation_field").

    Notes:
        This function assumes that the `representation_field` field in the table is compatible with 
        the shape of the representation data.
    
    Examples:
        >>> with tb.open_file('test_file.h5', mode='w') as h5file:
        ...     table_description = get_representation_table_description_from_data(np.random.rand(128, 256), representation_name='data')
        ...     table = h5file.create_table('/', 'test_table', table_description)
        ...     insert_representation_data(table, 'example.wav', 1.0, 0, np.random.rand(128, 256), representation_name='data')
        ...     table.nrows > 0 # doctest: +SKIP
        True
    """
    # Prepare the data to be inserted
    row = table.row
    row['filename'] = filename
    row['start'] = start
    row['id'] = table.nrows
    row['label'] = label
    row[representation_name] = representation_data.astype(np.float32)  # Ensure data is float32
    
    # Insert the data into the table
    row.append()
    
    # Save (commit) the changes
    table.flush()

def create_table(
    h5file: tb.File, 
    path: str, 
    table_description: tb.IsDescription,
    table_name: str = 'data'
) -> tb.Table:
    """
    Creates or retrieves a table within a given group path in an HDF5 file.
    
    Args:
        h5file: tables.File
            The open HDF5 file object.
        path: str
            The group path where the table should be located (e.g., "/train/fw").
        table_description: dict or tables.IsDescription
            The PyTables description of the table structure.
        table_name: str
            The name of the table to create or retrieve (Default is 'data').
    
    Returns:
        tables.Table
            The table object created or retrieved.
    
    Examples:
        >>> with tb.open_file('test_file.h5', mode='w') as h5file:
        ...     table_description = get_representation_table_description_from_data(np.random.rand(128, 256), representation_name='representation_field')
        ...     table = create_table(h5file, '/', table_description, 'test_table')
        ...     isinstance(table, tb.Table) # doctest: +SKIP
        True
    """
    # Define the filters
    filters = tb.Filters(complevel=1, complib='zlib', shuffle=True, fletcher32=True)

    
    full_path = f"{path}/{table_name}"  # Combine path and table name for creation

    # Create or get the table within the final group
    if not h5file.__contains__(full_path):
        # Create the table. 'createparents' will automatically create the parent groups if they do not yet exist
        table = h5file.create_table(path, table_name, table_description, filters=filters, chunkshape=(5,), createparents=True)
    else:
        table = h5file.get_node(full_path)
    
    return table

def save_attributes(node: tb.Leaf, attributes: dict[str, any]) -> None:
    """
    Save attributes to the given HDF5 leaf node.

    Args:
        node: tables.Leaf
            The PyTables leaf node (e.g., table or array) where the attributes will be saved.
        attributes: dict
            A dictionary of attributes to save, where keys are attribute names and values are attribute values.

    Examples:
        >>> with tb.open_file('test_file.h5', mode='w') as h5file:
        ...     array = h5file.create_array('/', 'test_array', obj=[1, 2, 3])
        ...     save_attributes(array, {'attribute1': 'value1', 'attribute2': 123})
        ...     array.attrs.attribute1 == 'value1' and array.attrs.attribute2 == 123 # doctest: +SKIP
        True
    """
    for key, value in attributes.items():
        node.attrs[key] = value