import pytest
import pandas as pd
from weather_loader import WeatherLoader

@pytest.fixture
def csv_file(tmp_path):
    content = "col1,col2\n1,2\n3,4"
    file_path = tmp_path / "test.csv"
    file_path.write_text(content)
    return file_path

def test_load_success(csv_file):
    loader = WeatherLoader(csv_file)
    df = loader.load()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_file_not_found():
    with pytest.raises(FileNotFoundError):
        loader = WeatherLoader("non_existent_file.csv")
        loader.load()
        
def test_exception():
    with pytest.raises(Exception):
        loader = WeatherLoader("non_existent_file.csv")
        loader.load()