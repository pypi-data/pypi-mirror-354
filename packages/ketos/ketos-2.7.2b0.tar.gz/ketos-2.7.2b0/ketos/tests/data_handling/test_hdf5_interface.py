import numpy as np
import tables as tb
import pytest
from ketos.data_handling.hdf5_interface import generate_table_description, insert_representation_data, save_attributes, create_table

######################## generate_table_description function ########################

def test_generate_table_description_returns_class():
    """Test that the function returns a class that is a subclass of `tb.IsDescription`."""
    sample = np.random.rand(128, 256)
    description = generate_table_description(sample, 'representation_field')
    
    # Check if the returned class is a subclass of `tb.IsDescription`
    assert issubclass(description, tb.IsDescription), "The returned description is not a subclass of `tb.IsDescription`"

def test_generate_table_description_has_correct_shape():
    """Test that the `data` field in the returned class has the correct shape."""
    sample_shape = (128, 256)
    sample = np.random.rand(*sample_shape)
    description = generate_table_description(sample, 'representation_field')
    
    # Check if the `data` field is present in the columns dictionary
    assert 'representation_field' in description.columns, "The `representation_field` field is missing in the generated table description"
    
    # Check if the `data` field has the correct shape
    assert description.columns['representation_field'].shape == sample_shape, f"Expected shape {sample_shape}, but got {description.columns['representation_field'].shape}"

def test_generate_table_description_field_types():
    # Create a sample array with a specific shape
    sample = np.random.rand(64, 128)
    
    # Generate the table description
    description = generate_table_description(sample, 'representation_field')
    
    # Verify the field types in the class definition directly
    assert isinstance(description.columns['filename'], tb.StringCol), "The `filename` field is not of type tb.StringCol"
    assert isinstance(description.columns['start'], tb.Float32Col), "The `start` field is not of type tb.Float32Col"
    assert isinstance(description.columns['id'], tb.UInt32Col), "The `id` field is not of type tb.UInt32Col"
    assert isinstance(description.columns['label'], tb.UInt8Col), "The `label` field is not of type tb.UInt8Col"
    assert isinstance(description.columns['representation_field'], tb.Float32Col), "The `'representation_field'` field is not of type tb.Float32Col"

@pytest.mark.parametrize("shape", [
    (1, 1),
    (10, 20),
    (128, 256, 3),
    (5,),
])
def test_generate_table_description_varied_shapes(shape):
    # Create a sample array with a several shapes shape
    sample = np.random.rand(*shape)
    
    # Generate the table description
    description = generate_table_description(sample, 'representation_field')
    
    # Check the representation_field field's shape matches the sample's shape
    assert description.columns['representation_field'].shape == shape, f"The shape of the `representation_field` field does not match the sample's shape {shape}"

def test_generate_table_description_empty_sample():
    """Test with an empty numpy array."""
    sample = np.array([])
    with pytest.raises(ValueError, match="The input data sample is empty. A non-empty array is required."):
        generate_table_description(sample, 'representation_field')

def test_generate_table_description_high_dimensional_sample():
    """Test with a high-dimensional numpy array."""
    sample = np.random.rand(4, 128, 256)
    description = generate_table_description(sample, 'representation_field')
    
    assert issubclass(description, tb.IsDescription), "The returned object should subclass `tb.IsDescription`"
    
    # Check if the representation_field field has the correct shape
    assert description.columns['representation_field'].shape == sample.shape, "The 'representation_field' field should have the correct shape"


def test_generate_table_description_single_dimensional_sample():
    """Test with a 1D numpy array."""
    sample = np.random.rand(100)
    description = generate_table_description(sample, 'representation_field')
    
    assert issubclass(description, tb.IsDescription), "The returned object should subclass `tb.IsDescription`"
    
    # Check if the representation_field field has the correct shape
    assert description.columns['representation_field'].shape == sample.shape, "The 'representation_field' field should have the correct shape"

def test_generate_table_description_scalar_sample():
    """Test with a scalar numpy array."""
    sample = np.array(42)
    description = generate_table_description(sample, 'representation_field')
    
    assert issubclass(description, tb.IsDescription), "The returned object should subclass `tb.IsDescription`"
    
    # Check if the representation_field field has the correct shape
    assert description.columns['representation_field'].shape == (), "The 'representation_field' field should have the correct scalar shape"

######################## insert_representation_data function ########################

@pytest.fixture
def sample_table(tmp_path):
    """Fixture to create a temporary HDF5 file and table for testing."""
    file_path = tmp_path / "test_file.h5"
    with tb.open_file(file_path, mode='w') as h5file:
        # Create a table description with a sample shape
        table_description = generate_table_description(np.random.rand(128, 256), 'representation_field')
        table = h5file.create_table('/', 'test_table', table_description)
        yield table  # Provide the table for the test
        table.flush()

def test_insert_representation_data_valid_input(sample_table):
    # Create sample input data
    filename = 'example.wav'
    offset = 1.0
    label = 0
    representation_data = np.random.rand(128, 256)
    representation_name = 'representation_field'

    # Insert data into the table
    insert_representation_data(sample_table, filename, offset, label, representation_data, representation_name=representation_name)

    # Verify that a row has been added
    assert sample_table.nrows == 1, "Row was not inserted correctly"

    # Verify the contents of the inserted row
    inserted_row = sample_table[0]  
    assert inserted_row['filename'].decode('utf-8') == filename, "Filename not inserted correctly"
    assert inserted_row['start'] == offset, "Start not inserted correctly"
    assert inserted_row['id'] == 0, "ID not assigned correctly"
    assert inserted_row['label'] == label, "Label not inserted correctly"
    np.testing.assert_array_almost_equal(inserted_row[representation_name], representation_data, err_msg="Representation data not inserted correctly")

def test_insert_representation_data_multiple_rows(sample_table):
    # Insert multiple rows into the table
    for i in range(5):
        filename = f'example_{i}.wav'
        offset = float(i)
        label = i % 2  # Alternate labels between 0 and 1
        representation_data = np.random.rand(128, 256).astype(np.float32)

        insert_representation_data(sample_table, filename, offset, label, representation_data, representation_name='representation_field')

    # Verify that five rows have been added
    assert sample_table.nrows == 5, "Not all rows were inserted correctly"

    # Verify the ID field increments correctly
    for i, row in enumerate(sample_table.iterrows()):
        assert row['id'] == i, f"Row ID {i} not set correctly"

def test_insert_representation_data_invalid_dtype(sample_table):
    # Create representation data with an invalid data type (e.g., int32)
    representation_data = np.random.randint(0, 255, (128, 256), dtype=np.int32)

    # Insert data and verify that it is correctly cast to float32
    insert_representation_data(sample_table, 'example.wav', 1.0, 0, representation_data, representation_name='representation_field')

    # Check that the data is in the correct dtype (float32) in the table
    inserted_row = sample_table.read(0)
    assert inserted_row['representation_field'].dtype == np.float32, "Representation data was not cast to float32"

def test_insert_representation_data_incompatible_shape(sample_table):
    """Test behavior when inserting data with an incompatible shape."""
    table = sample_table
    invalid_data_sample = np.random.rand(64, 128)  # Mismatched shape

    with pytest.raises(ValueError, match="could not broadcast input array"):
        insert_representation_data(table, "example.wav", 1.0, 0, invalid_data_sample, representation_name='representation_field')

def test_insert_representation_data_empty_data(sample_table):
    """Test behavior when inserting an empty numpy array."""
    table = sample_table
    empty_data_sample = np.array([])

    with pytest.raises(ValueError, match="could not broadcast input array from"):
        insert_representation_data(table, "example.wav", 1.0, 0, empty_data_sample)

######################## create_table function ########################

@pytest.fixture
def h5file_fixture(tmp_path):
    """Fixture to create a temporary HDF5 file."""
    file_path = tmp_path / "test_file.h5"
    with tb.open_file(file_path, mode='w') as h5file:
        yield h5file


def test_create_table_creates_new_table(h5file_fixture):
    """Test that a new table is created when it doesn't already exist."""
    h5file = h5file_fixture
    table_description = generate_table_description(np.random.rand(128, 256), 'representation_field')
    path = "/group"
    table_name = "test_table"

    table = create_table(h5file, path, table_description, table_name=table_name)

    # Verify the table is created and has the correct name
    assert isinstance(table, tb.Table), "The returned object should be a PyTables Table"
    assert table.name == table_name, "The table should have the specified name"
    assert h5file.__contains__(f"{path}/{table_name}"), "The table should exist in the HDF5 file"

def test_create_table_retrieves_existing_table(h5file_fixture):
    """Test that an existing table is retrieved instead of creating a new one."""
    h5file = h5file_fixture
    table_description = generate_table_description(np.random.rand(128, 256), 'representation_field')
    path = "/group"
    table_name = "test_table"

    # Create the table for the first time
    create_table(h5file, path, table_description, table_name=table_name)

    # Retrieve the existing table
    retrieved_table = create_table(h5file, path, table_description, table_name=table_name)

    # Verify that the retrieved table is the same as the originally created table
    assert isinstance(retrieved_table, tb.Table), "The returned object should be a PyTables Table"
    assert retrieved_table.name == table_name, "The table name should match the specified name"
    assert h5file.__contains__(f"{path}/{table_name}"), "The table should exist in the HDF5 file"

def test_create_table_creates_parent_groups(h5file_fixture):
    """Test that parent groups are automatically created if they do not exist."""
    h5file = h5file_fixture
    table_description = generate_table_description(np.random.rand(128, 256), 'representation_field')
    path = "/group/subgroup"
    table_name = "test_table"

    table = create_table(h5file, path, table_description, table_name=table_name)

    # Verify the parent group and table are created
    assert h5file.__contains__(path), "The parent group should be created"
    assert h5file.__contains__(f"{path}/{table_name}"), "The table should exist in the HDF5 file"

def test_create_table_with_invalid_path(h5file_fixture):
    """Test behavior when an invalid path is provided."""
    h5file = h5file_fixture
    table_description = generate_table_description(np.random.rand(128, 256), 'representation_field')
    path = "invalid_group"  # Not a valid group path (missing leading '/')
    table_name = "test_table"

    with pytest.raises(NameError, match="must start with a slash"):
        create_table(h5file, path, table_description, table_name=table_name)

######################## save_attributes function ########################

@pytest.fixture
def h5file_and_array(tmp_path):
    """Fixture to create a temporary HDF5 file and array for testing."""
    file_path = tmp_path / "test_file.h5"
    with tb.open_file(file_path, mode='w') as h5file:
        array = h5file.create_array('/', 'test_array', obj=[1, 2, 3])
        yield array


def test_save_attributes_valid(h5file_and_array):
    """Test saving valid attributes to an HDF5 leaf node."""
    array = h5file_and_array
    attributes = {
        'attribute1': 'value1',
        'attribute2': 123,
        'attribute3': [1, 2, 3],
        'attribute4': 3.14
    }

    save_attributes(array, attributes)

    # Verify the attributes are correctly saved
    for key, value in attributes.items():
        assert array.attrs[key] == value, f"The attribute '{key}' should have the value '{value}'"


def test_save_attributes_empty_dict(h5file_and_array):
    """Test saving an empty dictionary of attributes."""
    array = h5file_and_array
    attributes = {}

    save_attributes(array, attributes)

    # Verify no attributes are added
    assert len(array.attrs._f_list()) == 0, "No attributes should be saved for an empty dictionary"


def test_save_attributes_overwrite_existing(h5file_and_array):
    """Test overwriting existing attributes on a leaf node."""
    array = h5file_and_array
    initial_attributes = {'attribute1': 'initial_value'}
    save_attributes(array, initial_attributes)

    # Overwrite the attribute
    updated_attributes = {'attribute1': 'new_value'}
    save_attributes(array, updated_attributes)

    # Verify the attribute is updated
    assert array.attrs['attribute1'] == 'new_value', "The attribute should be overwritten with the new value"


def test_save_attributes_invalid_key(h5file_and_array):
    """Test behavior when using an invalid key."""
    array = h5file_and_array
    attributes = {123: 'value1'}  # Invalid key (not a string)

    with pytest.raises(TypeError, match="object name is not a string"):
        save_attributes(array, attributes)
