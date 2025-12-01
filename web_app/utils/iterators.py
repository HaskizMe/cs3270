"""
Module 4: Iterator and Generator implementations for weather data
"""
from collections.abc import Iterator


class WeatherDataIterator(Iterator):
    """
    Iterator that yields weather records one at a time
    Demonstrates Iterator pattern for Module 4
    """
    def __init__(self, weather_records):
        self.records = weather_records
        self.index = 0
        self.max_index = len(weather_records)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= self.max_index:
            raise StopIteration
        
        record = self.records[self.index]
        self.index += 1
        return record


def generate_weather_stats(weather_records):
    """
    Generator that yields summary statistics for each weather record
    Demonstrates Generator pattern for Module 4
    
    Args:
        weather_records: List of WeatherData model instances
        
    Yields:
        Dictionary with record summary statistics
    """
    for record in weather_records:
        # Calculate some basic stats for each record
        temp_range = None
        if record.min_temp is not None and record.max_temp is not None:
            temp_range = round(record.max_temp - record.min_temp, 2)
        
        yield {
            'location': record.location,
            'min_temp': record.min_temp,
            'max_temp': record.max_temp,
            'temp_range': temp_range,
            'rainfall': record.rainfall,
            'rain_today': record.rain_today
        }


def aggregate_stats_generator(weather_records):
    """
    Generator that yields aggregate statistics by location
    Demonstrates advanced Generator pattern for Module 4
    
    Args:
        weather_records: List of WeatherData model instances
        
    Yields:
        Dictionary with aggregated statistics per location
    """
    # Group records by location
    location_groups = {}
    for record in weather_records:
        location = record.location or 'Unknown'
        if location not in location_groups:
            location_groups[location] = []
        location_groups[location].append(record)
    
    # Yield statistics for each location
    for location, records in location_groups.items():
        temps = [r.min_temp for r in records if r.min_temp is not None]
        rainfalls = [r.rainfall for r in records if r.rainfall is not None]
        
        yield {
            'location': location,
            'record_count': len(records),
            'avg_min_temp': round(sum(temps) / len(temps), 2) if temps else None,
            'avg_rainfall': round(sum(rainfalls) / len(rainfalls), 2) if rainfalls else None
        }
