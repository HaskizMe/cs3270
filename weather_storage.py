class WeatherStorage:
    def __init__(self, out_file="descriptive_stats.csv"):
        self.out_file = out_file

    def save_stats(self, df):
        df.to_csv(self.out_file, index=False)
        print(f"Saved stats to {self.out_file}")
