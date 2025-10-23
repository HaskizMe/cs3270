# Weather Data Loader

## Overview
Loads a weather dataset (CSV) and prints out the top 10 rows.

## Environment
* Python: 3.12  
* Virtual Environment: `.venv` created with PyCharm  
* Dependencies: pandas, weather_stats, matplotlib, pytest 

## Setup
```bash
# create venv if needed
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install pandas matplotlib pytest

```

## How to build weather_stats module
```bash

python -m pip install --upgrade build
pip install setuptools wheel
python -m build

pip install twine # optional: for uploading to testPyPi
```


## Install weather_stats module (locally)
```bash

pip install dist/weather_stats_bh-0.1-py3-none-any.whl
```
> **Note:** If dist folder doesn't exist make sure to build the module before doing this with the commands above.

## Install weather_stats module (from testpypi)
```bash

pip install -i https://test.pypi.org/simple/ weather-stats-bh==0.1
```

## OOP Design

* WeatherLoader: Handles loading CSV data into a pandas DataFrame.
* WeatherProcessor (module): Contains the logic for calculating and printing descriptive statistics (mean, median, mode, range).
* WeatherStorage: Provides a simple way to save results to a CSV file.


## Module 4 (Iterators and Generators)

### Iterator Implementation
- **Location**: `WeatherStatsIterator` class in `weather_stats/stats.py`

### Generator Implementation
- **Location**: `generate_stats()` method in `WeatherProcessor` class

Both are demonstrated in the `print_descriptive_stats()` method.

## Module 5 (Testing)

### PyTest
- **Location**: `test_weather_loader.py`, `test_weather_storage.py`, `weather_stats/test_weather_stats.py`

- **Covers**: Saving stats to a CSV file, loading a CSV file, and printing descriptive statistics.


## Module 6 (Data Visualization)
- **Location**: `visualize_data()` method in `weather_stats/stats.py`

- **Covers**: Visualizing data as a bar chart.

- **Test**: `test_visualize_data_returns_correct_means` in `weather_stats/test_weather_stats.py`

## Module 7 (Concurrency)
- **Location**: `load_concurrent()` method in `weather_loader.py`

- **Covers**: Added the ability to load multiple CSV files concurrently using ThreadPoolExecutor.
