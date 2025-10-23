import logging
from pathlib import Path
import pandas as pd
from weather_loader import WeatherLoader
from weather_stats import WeatherProcessor, WeatherStatsIterator
from weather_storage import WeatherStorage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('weather_analysis.log')]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    folder = Path("weather_data")
    files = list(folder.glob("*.csv"))
    if not files:
        raise SystemExit(f"No CSV files found in {folder.resolve()}")

    try:
        # 1) Sequential load
        logger.info("Loading weather data (sequential)")
        loader = WeatherLoader(files[0])
        df_single = loader.load()
        logger.info(f"Sequential load OK: {len(df_single)} rows from {files[0].name}")

        # 2) Concurrent load
        logger.info("Loading weather data concurrently")
        multi_loader = WeatherLoader(files)
        dfs = multi_loader.load_concurrent(max_workers=4)
        logger.info(f"Concurrent load OK: {len(dfs)} files")

        # Combine all DataFrames before processing/saving
        combined_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Combined rows: {len(combined_df)}")

        # 3) Process data
        logger.info("Processing data")
        processor = WeatherProcessor(combined_df)
        processor.print_descriptive_stats()
        processor.visualize_data()

        # 4) Save stats
        logger.info("Saving statistics")
        storage = WeatherStorage()
        storage.save_stats(combined_df)

        # iterate a few rows using iterator
        it = WeatherStatsIterator(combined_df.head(5))
        for row in it:
            logger.debug(row)

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise