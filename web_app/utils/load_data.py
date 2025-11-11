"""
Script to load CSV weather data into the SQLite database
"""
import pandas as pd
from app import app, db
from models import WeatherData
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv_to_database(csv_path, batch_size=1000):
    """
    Load weather data from CSV file into database
    
    Args:
        csv_path: Path to the CSV file
        batch_size: Number of rows to insert at once (for performance)
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    logger.info(f"Loading data from {csv_path}")
    
    # Read CSV file
    df = pd.read_csv(csv_path)
    logger.info(f"Read {len(df)} rows from CSV")
    
    # Map CSV column names to database column names
    column_mapping = {
        'row ID': 'row_id',
        'Location': 'location',
        'MinTemp': 'min_temp',
        'MaxTemp': 'max_temp',
        'Rainfall': 'rainfall',
        'Evaporation': 'evaporation',
        'Sunshine': 'sunshine',
        'WindGustDir': 'wind_gust_dir',
        'WindGustSpeed': 'wind_gust_speed',
        'WindDir9am': 'wind_dir_9am',
        'WindDir3pm': 'wind_dir_3pm',
        'WindSpeed9am': 'wind_speed_9am',
        'WindSpeed3pm': 'wind_speed_3pm',
        'Humidity9am': 'humidity_9am',
        'Humidity3pm': 'humidity_3pm',
        'Pressure9am': 'pressure_9am',
        'Pressure3pm': 'pressure_3pm',
        'Cloud9am': 'cloud_9am',
        'Cloud3pm': 'cloud_3pm',
        'Temp9am': 'temp_9am',
        'Temp3pm': 'temp_3pm',
        'RainToday': 'rain_today',
        'RainTomorrow': 'rain_tomorrow'
    }
    
    # Rename columns to match database schema
    df = df.rename(columns=column_mapping)
    
    with app.app_context():
        # Clear existing data (optional)
        logger.info("Clearing existing data...")
        db.session.query(WeatherData).delete()
        db.session.commit()
        
        # Insert data in batches
        total_rows = len(df)
        inserted = 0
        
        for start_idx in range(0, total_rows, batch_size):
            end_idx = min(start_idx + batch_size, total_rows)
            batch = df.iloc[start_idx:end_idx]
            
            # Convert batch to list of dictionaries
            records = batch.to_dict('records')
            
            # Create WeatherData objects
            weather_objects = []
            for record in records:
                # Convert NaN to None for database
                cleaned_record = {k: (None if pd.isna(v) else v) for k, v in record.items()}
                
                # Create object with only the fields that exist in the model
                weather_obj = WeatherData(
                    location=cleaned_record.get('location'),
                    min_temp=cleaned_record.get('min_temp'),
                    max_temp=cleaned_record.get('max_temp'),
                    rainfall=cleaned_record.get('rainfall'),
                    evaporation=cleaned_record.get('evaporation'),
                    sunshine=cleaned_record.get('sunshine'),
                    wind_gust_dir=cleaned_record.get('wind_gust_dir'),
                    wind_gust_speed=cleaned_record.get('wind_gust_speed'),
                    wind_dir_9am=cleaned_record.get('wind_dir_9am'),
                    wind_dir_3pm=cleaned_record.get('wind_dir_3pm'),
                    wind_speed_9am=cleaned_record.get('wind_speed_9am'),
                    wind_speed_3pm=cleaned_record.get('wind_speed_3pm'),
                    humidity_9am=cleaned_record.get('humidity_9am'),
                    humidity_3pm=cleaned_record.get('humidity_3pm'),
                    pressure_9am=cleaned_record.get('pressure_9am'),
                    pressure_3pm=cleaned_record.get('pressure_3pm'),
                    cloud_9am=cleaned_record.get('cloud_9am'),
                    cloud_3pm=cleaned_record.get('cloud_3pm'),
                    temp_9am=cleaned_record.get('temp_9am'),
                    temp_3pm=cleaned_record.get('temp_3pm'),
                    rain_today=cleaned_record.get('rain_today'),
                    rain_tomorrow=cleaned_record.get('rain_tomorrow')
                )
                weather_objects.append(weather_obj)
            
            # Bulk insert
            db.session.bulk_save_objects(weather_objects)
            db.session.commit()
            
            inserted += len(weather_objects)
            logger.info(f"Inserted {inserted}/{total_rows} rows ({inserted/total_rows*100:.1f}%)")
        
        # Verify insertion
        count = db.session.query(WeatherData).count()
        logger.info(f"✓ Successfully loaded {count} rows into database")
        
        # Show sample data
        sample = db.session.query(WeatherData).limit(3).all()
        logger.info("\nSample records:")
        for record in sample:
            logger.info(f"  {record}")

if __name__ == '__main__':
    # Path to CSV file (in parent directory)
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'descriptive_stats.csv')
    csv_path = os.path.abspath(csv_path)
    
    try:
        load_csv_to_database(csv_path)
        logger.info("\n✓ Data loading complete!")
    except Exception as e:
        logger.error(f"Error loading data: {e}", exc_info=True)
        raise
