import pytest
import pandas as pd
import os
from weather_storage import WeatherStorage

@pytest.fixture
def sample_dataframe():
    """Creates a sample pandas DataFrame for testing."""
    data = {'col1': [1, 2], 'col2': [3, 4]}
    return pd.DataFrame(data)

def test_save_stats_success(sample_dataframe, tmp_path):
    """Tests that the save_stats method successfully saves a DataFrame to a CSV file."""
    # Create a temporary file path
    temp_file = tmp_path / "test_stats.csv"

    # Initialize WeatherStorage with the temporary file path
    storage = WeatherStorage(out_file=temp_file)

    # Save the dataframe
    storage.save_stats(sample_dataframe)

    # Check if the file was created
    assert os.path.exists(temp_file)

    # Read the file back and check if the content is correct
    saved_df = pd.read_csv(temp_file)
    pd.testing.assert_frame_equal(saved_df, sample_dataframe)
