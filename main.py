import logging
from weather_loader import WeatherLoader
from weather_stats import WeatherProcessor, WeatherStatsIterator
from weather_storage import WeatherStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('weather_analysis.log')
    ]
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:        
        # Load in weather training data
        logger.info("Loading weather data")
        loader = WeatherLoader("weather_data/Weather Training Data.csv")
        df = loader.load()
        logger.info(f"Successfully loaded data with {len(df)} rows")

        # Process raw data
        logger.info("Processing data")
        processor = WeatherProcessor(df)
        
        processor.print_descriptive_stats()
        # Visualize data
        processor.visualize_data()
        
        # Save to storage
        logger.info("Saving statistics")
        storage = WeatherStorage()
        storage.save_stats(df)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        raise