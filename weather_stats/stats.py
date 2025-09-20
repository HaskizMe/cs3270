import logging
from collections.abc import Iterator

logger = logging.getLogger(__name__)

class WeatherProcessor:
    def __init__(self, df):
        self.df = df
        logger.debug("Initialized WeatherProcessor")
        
    def __iter__(self):
        """Return iterator class"""
        return WeatherStatsIterator(self.df)
    
    def generate_stats(self):
        """Generator that yields statistics for each numeric column"""
        numeric_cols = self.df.select_dtypes(include="number").columns
        
        for col in numeric_cols:
            series = self.df[col].dropna()
            if series.empty:
                logger.warning(f"Column '{col}' contains no numeric data after dropping NA values")
                continue
                
            mode_val = series.mode()
            mode_str = mode_val.iloc[0] if not mode_val.empty else "N/A"
            
            stats = {
                'column': col,
                'mean': round(series.mean(), 2),
                'median': round(series.median(), 2),
                'mode': mode_str,
                'range': round(series.max() - series.min(), 2)
            }
            
            logger.debug(f"Generated stats for column '{col}': {stats}")
            yield stats

    def print_descriptive_stats(self):
        """Print descriptive statistics"""
        try:
            # Full statistics using generator
            for stats in self.generate_stats():
                print(f"\nColumn: {stats['column']}")
                print(f"  Mean   : {stats['mean']:.2f}")
                print(f"  Median : {stats['median']:.2f}")
                print(f"  Mode   : {stats['mode']}")
                print(f"  Range  : {stats['range']:.2f}")
                            
        except Exception as e:
            logger.error(f"Error calculating descriptive statistics: {str(e)}")
            raise


class WeatherStatsIterator(Iterator):
    """Iterator class for WeatherProcessor that iterates over weather statistics"""
    def __init__(self, df):
        self.df = df
        self.columns = df.select_dtypes(include="number").columns.tolist()
        self.current = 0
        self.max_index = len(self.columns)
        logger.debug("Initialized WeatherStatsIterator")
    
    def __next__(self):
        if self.current >= self.max_index:
            raise StopIteration
            
        col = self.columns[self.current]
        self.current += 1
        
        series = self.df[col].dropna() # Drop NA values
        if series.empty:
            logger.warning(f"Column '{col}' contains no numeric data after dropping NA values")
            return self.__next__()  # Skip to next column
            
        mode_val = series.mode()
        mode_str = mode_val.iloc[0] if not mode_val.empty else "N/A"
        
        return {
            'column': col,
            'mean': round(series.mean(), 2),
            'median': round(series.median(), 2),
            'mode': mode_str,
            'range': round(series.max() - series.min(), 2)
        }
