class WeatherProcessor:
    def __init__(self, df):
        self.df = df

    def print_descriptive_stats(self):
        numeric_cols = self.df.select_dtypes(include="number").columns

        print("\n=== Descriptive Statistics ===")
        for col in numeric_cols:
            series = self.df[col].dropna()
            if series.empty:
                continue
            mode_val = series.mode()
            mode_str = mode_val.iloc[0] if not mode_val.empty else "N/A"

            print(f"\nColumn: {col}")
            print(f"  Mean   : {series.mean():.2f}")
            print(f"  Median : {series.median():.2f}")
            print(f"  Mode   : {mode_str}")
            print(f"  Range  : {series.max() - series.min():.2f}")

