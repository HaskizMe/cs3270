"""
Module 6: Data Visualization using matplotlib
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web
import matplotlib.pyplot as plt
import io
import base64
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


def generate_temperature_chart(db_session, WeatherData, location=None):
    """
    Generate a bar chart showing average min and max temperatures.
    Similar to the console app's visualize_data() method.
    
    Args:
        db_session: Database session
        WeatherData: WeatherData model class
        location: Optional location filter
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Query average temperatures
        query = db_session.query(
            func.avg(WeatherData.min_temp).label('avg_min_temp'),
            func.avg(WeatherData.max_temp).label('avg_max_temp')
        )
        
        if location:
            query = query.filter(WeatherData.location == location)
        
        result = query.first()
        
        # Prepare data
        labels = ['Min Temperature', 'Max Temperature']
        values = [
            round(result.avg_min_temp, 2) if result.avg_min_temp else 0,
            round(result.avg_max_temp, 2) if result.avg_max_temp else 0
        ]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, values, color=['skyblue', 'coral'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}°C',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        title = f'Average Min and Max Temperature'
        if location:
            title += f' - {location}'
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        logger.info(f"Generated temperature chart for location: {location or 'All'}")
        
        return img_str
    
    except Exception as e:
        logger.error(f"Error generating temperature chart: {e}", exc_info=True)
        raise


def generate_rainfall_chart(db_session, WeatherData, limit=10):
    """
    Generate a bar chart showing average rainfall by location.
    
    Args:
        db_session: Database session
        WeatherData: WeatherData model class
        limit: Number of locations to include
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Query average rainfall by location
        results = db_session.query(
            WeatherData.location,
            func.avg(WeatherData.rainfall).label('avg_rainfall'),
            func.count(WeatherData.id).label('record_count')
        ).filter(
            WeatherData.location.isnot(None),
            WeatherData.rainfall.isnot(None)
        ).group_by(
            WeatherData.location
        ).order_by(
            func.avg(WeatherData.rainfall).desc()
        ).limit(limit).all()
        
        if not results:
            raise ValueError("No rainfall data available")
        
        # Prepare data
        locations = [r.location for r in results]
        rainfalls = [round(r.avg_rainfall, 2) for r in results]
        
        # Create bar chart
        plt.figure(figsize=(12, 6))
        bars = plt.bar(locations, rainfalls, color='steelblue')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=10)
        
        plt.title(f'Average Rainfall by Location (Top {limit})', fontsize=14, fontweight='bold')
        plt.xlabel('Location', fontsize=12)
        plt.ylabel('Average Rainfall (mm)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        logger.info(f"Generated rainfall chart for {len(results)} locations")
        
        return img_str
    
    except Exception as e:
        logger.error(f"Error generating rainfall chart: {e}", exc_info=True)
        raise


def generate_humidity_chart(db_session, WeatherData, location=None):
    """
    Generate a comparison chart for humidity at 9am vs 3pm.
    
    Args:
        db_session: Database session
        WeatherData: WeatherData model class
        location: Optional location filter
        
    Returns:
        Base64 encoded image string
    """
    try:
        # Query average humidity
        query = db_session.query(
            func.avg(WeatherData.humidity_9am).label('avg_humidity_9am'),
            func.avg(WeatherData.humidity_3pm).label('avg_humidity_3pm')
        )
        
        if location:
            query = query.filter(WeatherData.location == location)
        
        result = query.first()
        
        # Prepare data
        labels = ['9am Humidity', '3pm Humidity']
        values = [
            round(result.avg_humidity_9am, 2) if result.avg_humidity_9am else 0,
            round(result.avg_humidity_3pm, 2) if result.avg_humidity_3pm else 0
        ]
        
        # Create bar chart
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, values, color=['lightblue', 'lightcoral'])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        title = 'Average Humidity: 9am vs 3pm'
        if location:
            title += f' - {location}'
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylabel('Humidity (%)', fontsize=12)
        plt.ylim(0, 100)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=100, bbox_inches='tight')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        logger.info(f"Generated humidity chart for location: {location or 'All'}")
        
        return img_str
    
    except Exception as e:
        logger.error(f"Error generating humidity chart: {e}", exc_info=True)
        raise
