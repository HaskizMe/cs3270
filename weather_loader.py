import pandas as pd

class WeatherLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        try:
            df = pd.read_csv(self.file_path)
            return df
        except FileNotFoundError:
            raise
        except Exception:
            raise