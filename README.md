# Weather Data Loader

## Overview

Loads a weather dataset (CSV) and prints out the top 10 rows.

## Environment

-   Python: 3.12
-   Virtual Environment: `.venv` created with PyCharm
-   Dependencies: pandas, weather_stats, matplotlib, pytest

## Setup

```bash
# create venv if needed
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install pandas matplotlib pytest Flask Flask-SQLAlchemy

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

-   WeatherLoader: Handles loading CSV data into a pandas DataFrame.
-   WeatherProcessor (module): Contains the logic for calculating and printing descriptive statistics (mean, median, mode, range).
-   WeatherStorage: Provides a simple way to save results to a CSV file.

## Module 4 (Iterators and Generators)

### Iterator Implementation

-   **Location**: `WeatherStatsIterator` class in `weather_stats/stats.py`

### Generator Implementation

-   **Location**: `generate_stats()` method in `WeatherProcessor` class

Both are demonstrated in the `print_descriptive_stats()` method.

## Module 5 (Testing)

### PyTest

-   **Location**: `test_weather_loader.py`, `test_weather_storage.py`, `weather_stats/test_weather_stats.py`

-   **Covers**: Saving stats to a CSV file, loading a CSV file, and printing descriptive statistics.

## Module 6 (Data Visualization)

-   **Location**: `visualize_data()` method in `weather_stats/stats.py`

-   **Covers**: Visualizing data as a bar chart.

-   **Test**: `test_visualize_data_returns_correct_means` in `weather_stats/test_weather_stats.py`

## Module 7 (Concurrency)

-   **Location**: `load_concurrent()` method in `weather_loader.py`

-   **Covers**: Added the ability to load multiple CSV files concurrently using ThreadPoolExecutor.

## Module 8 (PySpark)

-   **File Location**: `notebooks/Module_8_pyspark.ipynb` (Open notebook in google collab changes can be found in the notebook) [Google Collab Project](https://colab.research.google.com/drive/1w-dgeYc4opu230ykoIfMdx9Cgh9b6CZe#scrollTo=E96mC78N3mZh)

### Changes/modifications:

#### weather_loader.py

-   Modified to use PySpark instead of Pandas to load the data.
-   Removed the `load_concurrent()` method since pyspark isn't thread safe

#### stats.py

-   Updated `WeatherProcessor` numeric column detection from select_dtypes() to Spark schema inspection (NumericType) since Pandas helpers don’t exist in Spark.
-   Replaced Pandas operations (mean, median, mode, range) with Spark equivalents (F.avg, F.min, F.max, approxQuantile, groupBy().count()).
-   Used .collect() only on small aggregated results, because Spark computations are lazy and distributed.
-   Visualization now uses Spark to aggregate values first, then collects a tiny result to plot locally—matplotlib cannot operate on Spark DataFrames directly.
-   Pandas is only used for lightweight plotting support because PySpark cannot interface directly with matplotlib. All core data processing, statistics, and transformations are handled entirely in PySpark.

#### weather_storage.py

-   Replaced to_csv() (Pandas-only) with df.write.csv() (PySpark).
-   Added .option("header", True) to include headers like Pandas.
-   Added .mode("overwrite") to match typical overwrite behavior.
-   Added .coalesce(1) optionally to write a single CSV file instead of many tiny partitioned files.

## Module 9 (3 tier Web App)

### Setup

```bash
# create venv if needed
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install pandas matplotlib pytest Flask Flask-SQLAlchemy
```

### **Folder Location**: `web_app/`

### How to run

-   Navigate to web_app directory `cd web_app`
-   Run `python app.py`
-   Open `http://localhost:5001` in your browser
