from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    """SQLAlchemy model for weather data"""
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    location = db.Column(db.String(100))
    min_temp = db.Column(db.Float)
    max_temp = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    evaporation = db.Column(db.Float)
    sunshine = db.Column(db.Float)
    wind_gust_dir = db.Column(db.String(10))
    wind_gust_speed = db.Column(db.Float)
    wind_dir_9am = db.Column(db.String(10))
    wind_dir_3pm = db.Column(db.String(10))
    wind_speed_9am = db.Column(db.Float)
    wind_speed_3pm = db.Column(db.Float)
    humidity_9am = db.Column(db.Float)
    humidity_3pm = db.Column(db.Float)
    pressure_9am = db.Column(db.Float)
    pressure_3pm = db.Column(db.Float)
    cloud_9am = db.Column(db.Float)
    cloud_3pm = db.Column(db.Float)
    temp_9am = db.Column(db.Float)
    temp_3pm = db.Column(db.Float)
    rain_today = db.Column(db.String(5))
    rain_tomorrow = db.Column(db.String(5))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'date': self.date,
            'location': self.location,
            'min_temp': self.min_temp,
            'max_temp': self.max_temp,
            'rainfall': self.rainfall,
            'evaporation': self.evaporation,
            'sunshine': self.sunshine,
            'wind_gust_dir': self.wind_gust_dir,
            'wind_gust_speed': self.wind_gust_speed,
            'wind_dir_9am': self.wind_dir_9am,
            'wind_dir_3pm': self.wind_dir_3pm,
            'wind_speed_9am': self.wind_speed_9am,
            'wind_speed_3pm': self.wind_speed_3pm,
            'humidity_9am': self.humidity_9am,
            'humidity_3pm': self.humidity_3pm,
            'pressure_9am': self.pressure_9am,
            'pressure_3pm': self.pressure_3pm,
            'cloud_9am': self.cloud_9am,
            'cloud_3pm': self.cloud_3pm,
            'temp_9am': self.temp_9am,
            'temp_3pm': self.temp_3pm,
            'rain_today': self.rain_today,
            'rain_tomorrow': self.rain_tomorrow
        }
    
    def __repr__(self):
        return f'<WeatherData {self.date} - {self.location}>'


# Note: db is initialized here but will be configured with app in app.py
# This avoids circular imports