import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
from pathlib import Path
from collections.abc import Iterable

class WeatherLoader:
    def __init__(self, file_paths):
        # Always store as a list of strings
        if isinstance(file_paths, (str, Path)):
            self.file_paths = [str(file_paths)]
        elif isinstance(file_paths, Iterable):
            self.file_paths = [str(p) for p in file_paths]
        else:
            raise TypeError("file_paths must be a path or an iterable of paths/strings")

    def load(self):
        """Sequentially load one CSV file (original behavior)."""
        path = self.file_paths[0]
        try:
            df = pd.read_csv(path)
            return df
        except Exception as e:
            print(f"Error loading {path}: {e}")
            raise

    def load_concurrent(self, max_workers: int = 3):
        """Load multiple CSV files concurrently (I/O concurrency)."""
        start = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            dfs = list(executor.map(pd.read_csv, self.file_paths))
        print(f"Loaded {len(dfs)} files concurrently in {time.time() - start:.2f} seconds")
        return dfs