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
from models import db
db.init_app(app)

# Routes
@app.route('/api')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['GET'])
def get_weather_data():
    """API endpoint to fetch weather data with optional filters"""
    # Will implement filtering in later steps
    return jsonify({'message': 'Weather data endpoint - to be implemented'})

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """API endpoint to fetch statistics for weather data"""
    # Will implement statistics in later steps
    return jsonify({'message': 'Statistics endpoint - to be implemented'})

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        from models import WeatherData
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