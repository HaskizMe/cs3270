import pytest
import pandas as pd
import numpy as np
from weather_stats.stats import WeatherStatsIterator, WeatherProcessor

@pytest.fixture
def sample_dataframe():
    """Creates a sample DataFrame for testing the stats module."""
    data = {
        'temp': [10, 20, 30, np.nan],
        'humidity': [50, 55, 60, 58],
        'location': ['A', 'B', 'C', 'D'],
        'empty_col': [np.nan, np.nan, np.nan, np.nan]
    }
    return pd.DataFrame(data)

def test_weather_stats_iterator(sample_dataframe):
    """Tests the basic functionality of the WeatherStatsIterator."""
    iterator = WeatherStatsIterator(sample_dataframe)

    # First column: 'temp'
    stats1 = next(iterator)
    assert stats1['column'] == 'temp'
    assert stats1['mean'] == 20.0
    assert stats1['median'] == 20.0
    assert stats1['range'] == 20.0

    # Second column: 'humidity'
    stats2 = next(iterator)
    assert stats2['column'] == 'humidity'
    assert stats2['mean'] == 55.75
    assert stats2['median'] == 56.5
    assert stats2['range'] == 10.0

    # After the last valid column, it should raise StopIteration
    with pytest.raises(StopIteration):
        next(iterator)

def test_generate_stats_generator(sample_dataframe):
    """Tests the generate_stats generator in WeatherProcessor."""
    processor = WeatherProcessor(sample_dataframe)
    stats_generator = processor.generate_stats()

    # Convert generator to a list to easily check the results
    stats_list = list(stats_generator)

    # Should only generate stats for the two valid numeric columns
    assert len(stats_list) == 2

    # Check the stats for the first column ('temp')
    stats1 = stats_list[0]
    assert stats1['column'] == 'temp'
    assert stats1['mean'] == 20.0

    # Check the stats for the second column ('humidity')
    stats2 = stats_list[1]
    assert stats2['column'] == 'humidity'
    assert stats2['mean'] == 55.75

def test_print_descriptive_stats(sample_dataframe, capsys):
    """Tests that print_descriptive_stats prints the correct output."""
    processor = WeatherProcessor(sample_dataframe)
    processor.print_descriptive_stats()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Check for temp stats
    assert "Column: temp" in output
    assert "Mean   : 20.00" in output
    assert "Median : 20.00" in output
    assert "Range  : 20.00" in output

    # Check for humidity stats
    assert "Column: humidity" in output
    assert "Mean   : 55.75" in output
    assert "Median : 56.50" in output
    assert "Range  : 10.00" in output