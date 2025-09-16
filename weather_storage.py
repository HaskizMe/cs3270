import logging

logger = logging.getLogger(__name__)

class WeatherStorage:
    def __init__(self, out_file="descriptive_stats.csv"):
        self.out_file = out_file

    def save_stats(self, df):
        try:
            df.to_csv(self.out_file, index=False)
            logger.info(f"Successfully saved statistics to {self.out_file}")
        except Exception:
            raise
