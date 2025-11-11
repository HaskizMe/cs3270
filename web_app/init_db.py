"""
Database initialization and verification script
"""
from app import app, db
from models import WeatherData

def init_database():
    """Initialize the database and create tables"""
    with app.app_context():
        # Drop all tables (optional - for clean start)
        db.drop_all()
        
        # Create all tables
        db.create_all()
        print("Database tables created successfully")
        
        # Verify table structure
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n✓ Tables in database: {tables}")
        
        if 'weather_data' in tables:
            columns = inspector.get_columns('weather_data')
            print(f"\n✓ Columns in 'weather_data' table:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
        
        # Check row count
        count = db.session.query(WeatherData).count()
        print(f"\n✓ Current row count: {count}")

if __name__ == '__main__':
    init_database()
