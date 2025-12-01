"""
Module 7: Concurrency implementation using ThreadPoolExecutor
"""
from concurrent.futures import ThreadPoolExecutor
import time
import logging
from sqlalchemy import and_

logger = logging.getLogger(__name__)


def process_location_stats(location, db_session, WeatherData):
    """
    Process statistics for a single location.
    This function will be executed concurrently for multiple locations.
    
    Args:
        location: Location name to process
        db_session: Database session
        WeatherData: WeatherData model class
        
    Returns:
        Dictionary with location statistics
    """
    start_time = time.time()
    
    # Query all records for this location
    records = db_session.query(WeatherData).filter(
        WeatherData.location == location
    ).all()
    
    if not records:
        return {
            'location': location,
            'error': 'No records found',
            'processing_time': 0
        }
    
    # Calculate statistics
    temps = [r.min_temp for r in records if r.min_temp is not None]
    max_temps = [r.max_temp for r in records if r.max_temp is not None]
    rainfalls = [r.rainfall for r in records if r.rainfall is not None]
    
    processing_time = time.time() - start_time
    
    return {
        'location': location,
        'record_count': len(records),
        'avg_min_temp': round(sum(temps) / len(temps), 2) if temps else None,
        'avg_max_temp': round(sum(max_temps) / len(max_temps), 2) if max_temps else None,
        'avg_rainfall': round(sum(rainfalls) / len(rainfalls), 2) if rainfalls else None,
        'processing_time': round(processing_time, 4)
    }


def process_locations_concurrently(locations, db_session, WeatherData, max_workers=4):
    """
    Process statistics for multiple locations concurrently using ThreadPoolExecutor.
    Demonstrates I/O concurrency similar to the console app's concurrent CSV loading.
    
    Args:
        locations: List of location names to process
        db_session: Database session
        WeatherData: WeatherData model class
        max_workers: Maximum number of concurrent threads (default: 4)
        
    Returns:
        Tuple of (results list, total processing time)
    """
    start_time = time.time()
    
    # Use ThreadPoolExecutor to process locations concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = [
            executor.submit(process_location_stats, location, db_session, WeatherData)
            for location in locations
        ]
        
        # Collect results as they complete
        results = [future.result() for future in futures]
    
    total_time = time.time() - start_time
    
    logger.info(f"Processed {len(locations)} locations concurrently in {total_time:.2f} seconds")
    
    return results, round(total_time, 4)


def process_locations_sequentially(locations, db_session, WeatherData):
    """
    Process statistics for multiple locations sequentially (for comparison).
    
    Args:
        locations: List of location names to process
        db_session: Database session
        WeatherData: WeatherData model class
        
    Returns:
        Tuple of (results list, total processing time)
    """
    start_time = time.time()
    
    results = []
    for location in locations:
        result = process_location_stats(location, db_session, WeatherData)
        results.append(result)
    
    total_time = time.time() - start_time
    
    logger.info(f"Processed {len(locations)} locations sequentially in {total_time:.2f} seconds")
    
    return results, round(total_time, 4)


def fetch_location_data(location, filters, app, db, WeatherData):
    """
    Fetch weather data for a single location with filters.
    This function will be executed concurrently for multiple locations.
    
    Args:
        location: Location name to fetch data for
        filters: Dictionary of filter parameters
        app: Flask application instance
        db: SQLAlchemy database instance
        WeatherData: WeatherData model class
        
    Returns:
        Dictionary with location and its weather records
    """
    # Each thread needs its own application context
    with app.app_context():
        # Build query for this location
        query = db.session.query(WeatherData).filter(WeatherData.location == location)
        
        # Apply temperature filters
        if filters.get('min_temp_min') is not None:
            query = query.filter(WeatherData.min_temp >= filters['min_temp_min'])
        if filters.get('min_temp_max') is not None:
            query = query.filter(WeatherData.min_temp <= filters['min_temp_max'])
        if filters.get('max_temp_min') is not None:
            query = query.filter(WeatherData.max_temp >= filters['max_temp_min'])
        if filters.get('max_temp_max') is not None:
            query = query.filter(WeatherData.max_temp <= filters['max_temp_max'])
        
        # Apply rain filter
        if filters.get('rain_today'):
            query = query.filter(WeatherData.rain_today == filters['rain_today'])
        
        # Apply limit for this location
        limit_per_location = filters.get('limit_per_location', 10)
        results = query.limit(limit_per_location).all()
        
        # Convert to dictionaries
        return {
            'location': location,
            'count': len(results),
            'records': [record.to_dict() for record in results]
        }


def fetch_weather_data_concurrently(locations, filters, app, db, WeatherData, max_workers=4):
    """
    Fetch weather data for multiple locations concurrently.
    This demonstrates I/O concurrency when filtering and fetching data.
    
    Args:
        locations: List of location names to fetch data for
        filters: Dictionary of filter parameters
        app: Flask application instance
        db: SQLAlchemy database instance
        WeatherData: WeatherData model class
        max_workers: Maximum number of concurrent threads
        
    Returns:
        Tuple of (combined results list, metadata dict)
    """
    start_time = time.time()
    
    # Use ThreadPoolExecutor to fetch data from multiple locations concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_location_data, location, filters, app, db, WeatherData)
            for location in locations
        ]
        
        # Collect results
        location_results = [future.result() for future in futures]
    
    # Combine all records from all locations
    all_records = []
    for loc_result in location_results:
        all_records.extend(loc_result['records'])
    
    total_time = time.time() - start_time
    
    metadata = {
        'concurrent_processing': True,
        'locations_processed': len(locations),
        'max_workers': max_workers,
        'processing_time': round(total_time, 4),
        'total_records': len(all_records),
        'location_breakdown': [
            {'location': lr['location'], 'count': lr['count']} 
            for lr in location_results
        ]
    }
    
    logger.info(f"Fetched data from {len(locations)} locations concurrently in {total_time:.4f} seconds")
    
    return all_records, metadata
