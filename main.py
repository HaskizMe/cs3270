from weather_loader import WeatherLoader
from weather_stats import WeatherProcessor
from weather_storage import WeatherStorage

if __name__ == "__main__":
    # Load in weather training data
    loader = WeatherLoader("weather_data/Weather Training Data.csv")
    df = loader.load()

    # Process raw data
    processor = WeatherProcessor(df)
    processor.print_descriptive_stats()

    # Save to storage
    storage = WeatherStorage()
    storage.save_stats(df)