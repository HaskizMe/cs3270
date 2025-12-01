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

@app.route('/api/module4/demo', methods=['GET'])
def module4_demo():
    """
    Module 4: Demonstrates Iterator and Generator patterns
    
    Query Parameters:
    - limit: Number of records to process (default: 10)
    """
    try:
        from utils.iterators import WeatherDataIterator, generate_weather_stats, aggregate_stats_generator
        
        limit = min(request.args.get('limit', 10, type=int), 100)
        
        # Fetch sample data
        records = db.session.query(WeatherData).limit(limit).all()
        
        if not records:
            return jsonify({
                'success': False,
                'error': 'No weather data found in database'
            }), 404
        
        # Demonstrate Iterator pattern
        iterator = WeatherDataIterator(records)
        iterator_results = []
        for record in iterator:
            iterator_results.append({
                'id': record.id,
                'location': record.location,
                'min_temp': record.min_temp
            })
        
        # Demonstrate Generator pattern - individual stats
        generator_results = list(generate_weather_stats(records))
        
        # Demonstrate Generator pattern - aggregate stats
        aggregate_results = list(aggregate_stats_generator(records))
        
        return jsonify({
            'success': True,
            'message': 'Module 4: Iterator and Generator demonstration',
            'record_count': len(records),
            'iterator_demo': {
                'description': 'Iterator pattern: Iterates through weather records',
                'sample_results': iterator_results[:5]  # Show first 5
            },
            'generator_demo': {
                'description': 'Generator pattern: Yields weather statistics on-demand',
                'sample_results': generator_results[:5]  # Show first 5
            },
            'aggregate_generator_demo': {
                'description': 'Generator pattern: Yields aggregated stats by location',
                'results': aggregate_results
            }
        })
    
    except Exception as e:
        logger.error(f"Error in Module 4 demo: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/weather/concurrent', methods=['GET'])
def get_weather_concurrent():
    """
    Module 7: Fetch weather data using concurrent processing by location
    Demonstrates concurrency when filtering and fetching data
    
    Query Parameters:
    - min_temp_min, min_temp_max: Temperature range filters
    - max_temp_min, max_temp_max: Temperature range filters
    - rain_today: Filter by rain today (Yes/No)
    - limit_per_location: Records per location (default: 10)
    - max_workers: Number of concurrent threads (default: 4)
    """
    try:
        from utils.concurrency import fetch_weather_data_concurrently
        
        # Get all locations or a subset
        all_locations = db.session.query(WeatherData.location)\
            .distinct()\
            .filter(WeatherData.location.isnot(None))\
            .limit(10)\
            .all()
        
        location_list = [loc[0] for loc in all_locations]
        
        if not location_list:
            return jsonify({
                'success': False,
                'error': 'No locations found in database'
            }), 404
        
        # Build filters from query parameters
        filters = {
            'min_temp_min': request.args.get('min_temp_min', type=float),
            'min_temp_max': request.args.get('min_temp_max', type=float),
            'max_temp_min': request.args.get('max_temp_min', type=float),
            'max_temp_max': request.args.get('max_temp_max', type=float),
            'rain_today': request.args.get('rain_today'),
            'limit_per_location': request.args.get('limit_per_location', 10, type=int)
        }
        
        max_workers = min(request.args.get('max_workers', 4, type=int), 10)
        
        # Fetch data concurrently across all locations
        # Pass app and db instances for proper application context in threads
        records, metadata = fetch_weather_data_concurrently(
            location_list, filters, app, db, WeatherData, max_workers
        )
        
        return jsonify({
            'success': True,
            'message': 'Weather data fetched using concurrent processing',
            'count': len(records),
            'data': records,
            'metadata': metadata,
            'info': f'Processed {metadata["locations_processed"]} locations concurrently in {metadata["processing_time"]}s using {metadata["max_workers"]} workers'
        })
    
    except Exception as e:
        logger.error(f"Error in concurrent weather fetch: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/module7/demo', methods=['GET'])
def module7_demo():
    """
    Module 7: Demonstrates Concurrency using ThreadPoolExecutor
    Processes statistics for multiple locations concurrently vs sequentially
    
    Query Parameters:
    - max_workers: Number of concurrent threads (default: 4, max: 10)
    - compare: If 'true', also runs sequential processing for comparison
    """
    try:
        from utils.concurrency import process_locations_concurrently, process_locations_sequentially
        
        # Get all unique locations
        locations = db.session.query(WeatherData.location)\
            .distinct()\
            .filter(WeatherData.location.isnot(None))\
            .limit(10)\
            .all()
        
        location_list = [loc[0] for loc in locations]
        
        if not location_list:
            return jsonify({
                'success': False,
                'error': 'No locations found in database'
            }), 404
        
        max_workers = min(request.args.get('max_workers', 4, type=int), 10)
        compare = request.args.get('compare', 'false').lower() == 'true'
        
        # Process locations concurrently
        concurrent_results, concurrent_time = process_locations_concurrently(
            location_list, db.session, WeatherData, max_workers
        )
        
        response = {
            'success': True,
            'message': 'Module 7: Concurrency demonstration using ThreadPoolExecutor',
            'concurrent_processing': {
                'description': f'Processed {len(location_list)} locations using {max_workers} workers',
                'max_workers': max_workers,
                'total_time': concurrent_time,
                'results': concurrent_results
            }
        }
        
        # Optional: Compare with sequential processing
        if compare:
            sequential_results, sequential_time = process_locations_sequentially(
                location_list, db.session, WeatherData
            )
            
            speedup = round(sequential_time / concurrent_time, 2) if concurrent_time > 0 else 0
            
            response['sequential_processing'] = {
                'description': f'Processed {len(location_list)} locations sequentially',
                'total_time': sequential_time,
                'results': sequential_results
            }
            response['comparison'] = {
                'speedup_factor': f"{speedup}x faster",
                'time_saved': round(sequential_time - concurrent_time, 4)
            }
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error in Module 7 demo: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visualize/temperature', methods=['GET'])
def visualize_temperature():
    """
    Module 6: Generate temperature visualization chart
    
    Query Parameters:
    - location: Optional location filter
    """
    try:
        from utils.visualization import generate_temperature_chart
        
        location = request.args.get('location')
        
        # Generate chart
        img_str = generate_temperature_chart(db.session, WeatherData, location)
        
        return jsonify({
            'success': True,
            'message': 'Module 6: Temperature visualization generated',
            'chart_type': 'temperature',
            'location': location or 'All locations',
            'image': img_str
        })
    
    except Exception as e:
        logger.error(f"Error generating temperature visualization: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visualize/rainfall', methods=['GET'])
def visualize_rainfall():
    """
    Module 6: Generate rainfall visualization chart
    
    Query Parameters:
    - limit: Number of locations to show (default: 10)
    """
    try:
        from utils.visualization import generate_rainfall_chart
        
        limit = min(request.args.get('limit', 10, type=int), 20)
        
        # Generate chart
        img_str = generate_rainfall_chart(db.session, WeatherData, limit)
        
        return jsonify({
            'success': True,
            'message': 'Module 6: Rainfall visualization generated',
            'chart_type': 'rainfall',
            'locations_shown': limit,
            'image': img_str
        })
    
    except Exception as e:
        logger.error(f"Error generating rainfall visualization: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/visualize/humidity', methods=['GET'])
def visualize_humidity():
    """
    Module 6: Generate humidity visualization chart
    
    Query Parameters:
    - location: Optional location filter
    """
    try:
        from utils.visualization import generate_humidity_chart
        
        location = request.args.get('location')
        
        # Generate chart
        img_str = generate_humidity_chart(db.session, WeatherData, location)
        
        return jsonify({
            'success': True,
            'message': 'Module 6: Humidity visualization generated',
            'chart_type': 'humidity',
            'location': location or 'All locations',
            'image': img_str
        })
    
    except Exception as e:
        logger.error(f"Error generating humidity visualization: {e}", exc_info=True)
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