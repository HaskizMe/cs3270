from flask import Flask, render_template, request, jsonify
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "weather.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Import models and initialize SQLAlchemy with app
from models import db, WeatherData
from sqlalchemy import func
db.init_app(app)

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    """
    API endpoint to fetch weather data with optional filters
    
    Query Parameters:
    - location: Filter by location name
    - min_temp_min: Minimum temperature lower bound
    - min_temp_max: Minimum temperature upper bound
    - max_temp_min: Maximum temperature lower bound
    - max_temp_max: Maximum temperature upper bound
    - rain_today: Filter by rain today (Yes/No)
    - limit: Number of records to return (default: 100, max: 1000)
    - offset: Number of records to skip (for pagination)
    """
    try:
        # Start with base query
        query = db.session.query(WeatherData)
        
        # Apply filters based on query parameters
        location = request.args.get('location')
        if location:
            query = query.filter(WeatherData.location == location)
        
        # Temperature filters
        min_temp_min = request.args.get('min_temp_min', type=float)
        if min_temp_min is not None:
            query = query.filter(WeatherData.min_temp >= min_temp_min)
        
        min_temp_max = request.args.get('min_temp_max', type=float)
        if min_temp_max is not None:
            query = query.filter(WeatherData.min_temp <= min_temp_max)
        
        max_temp_min = request.args.get('max_temp_min', type=float)
        if max_temp_min is not None:
            query = query.filter(WeatherData.max_temp >= max_temp_min)
        
        max_temp_max = request.args.get('max_temp_max', type=float)
        if max_temp_max is not None:
            query = query.filter(WeatherData.max_temp <= max_temp_max)
        
        # Rain filter
        rain_today = request.args.get('rain_today')
        if rain_today:
            query = query.filter(WeatherData.rain_today == rain_today)
        
        # Pagination
        limit = min(request.args.get('limit', 100, type=int), 1000)
        offset = request.args.get('offset', 0, type=int)
        
        # Get total count before pagination
        total_count = query.count()
        
        # Apply pagination
        results = query.limit(limit).offset(offset).all()
        
        # Convert to dictionary
        data = [record.to_dict() for record in results]
        
        return jsonify({
            'success': True,
            'count': len(data),
            'total': total_count,
            'limit': limit,
            'offset': offset,
            'data': data
        })
    
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """
    API endpoint to fetch aggregated statistics
    
    Query Parameters:
    - location: Filter statistics by location
    """
    try:
        # Base query
        query = db.session.query(
            func.count(WeatherData.id).label('total_records'),
            func.avg(WeatherData.min_temp).label('avg_min_temp'),
            func.avg(WeatherData.max_temp).label('avg_max_temp'),
            func.min(WeatherData.min_temp).label('lowest_temp'),
            func.max(WeatherData.max_temp).label('highest_temp'),
            func.avg(WeatherData.rainfall).label('avg_rainfall'),
            func.avg(WeatherData.humidity_9am).label('avg_humidity_9am'),
            func.avg(WeatherData.humidity_3pm).label('avg_humidity_3pm'),
            func.avg(WeatherData.pressure_9am).label('avg_pressure_9am'),
            func.avg(WeatherData.pressure_3pm).label('avg_pressure_3pm')
        )
        
        # Filter by location if provided
        location = request.args.get('location')
        if location:
            query = query.filter(WeatherData.location == location)
        
        result = query.first()
        
        stats = {
            'success': True,
            'location': location if location else 'All locations',
            'statistics': {
                'total_records': result.total_records,
                'avg_min_temp': round(result.avg_min_temp, 2) if result.avg_min_temp else None,
                'avg_max_temp': round(result.avg_max_temp, 2) if result.avg_max_temp else None,
                'lowest_temp': round(result.lowest_temp, 2) if result.lowest_temp else None,
                'highest_temp': round(result.highest_temp, 2) if result.highest_temp else None,
                'avg_rainfall': round(result.avg_rainfall, 2) if result.avg_rainfall else None,
                'avg_humidity_9am': round(result.avg_humidity_9am, 2) if result.avg_humidity_9am else None,
                'avg_humidity_3pm': round(result.avg_humidity_3pm, 2) if result.avg_humidity_3pm else None,
                'avg_pressure_9am': round(result.avg_pressure_9am, 2) if result.avg_pressure_9am else None,
                'avg_pressure_3pm': round(result.avg_pressure_3pm, 2) if result.avg_pressure_3pm else None
            }
        }
        
        return jsonify(stats)
    
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get list of unique locations in the database"""
    try:
        locations = db.session.query(WeatherData.location)\
            .distinct()\
            .order_by(WeatherData.location)\
            .all()
        
        location_list = [loc[0] for loc in locations if loc[0]]
        
        return jsonify({
            'success': True,
            'count': len(location_list),
            'locations': location_list
        })
    
    except Exception as e:
        logger.error(f"Error fetching locations: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")
        
        # Check if database is empty and load data if needed
        row_count = db.session.query(WeatherData).count()
        if row_count == 0:
            logger.info("Database is empty. Loading data from CSV...")
            try:
                from utils.load_data import load_csv_to_database
                csv_path = os.path.join(basedir, '..', 'descriptive_stats.csv')
                csv_path = os.path.abspath(csv_path)
                load_csv_to_database(csv_path)
                logger.info("Data loaded successfully!")
            except Exception as e:
                logger.warning(f"Could not load data automatically: {e}")
                logger.info("You can manually load data by running: python load_data.py")
        else:
            logger.info(f"Database contains {row_count} weather records")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5001)