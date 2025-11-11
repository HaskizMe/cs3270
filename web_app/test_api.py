"""
Test script to verify API endpoints
Run this after starting the Flask server with: python app.py
"""
import requests
import json

BASE_URL = "http://localhost:5001"

def test_locations():
    """Test the locations endpoint"""
    print("\n=== Testing /api/locations ===")
    response = requests.get(f"{BASE_URL}/api/locations")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Number of locations: {data.get('count')}")
    print(f"First 5 locations: {data.get('locations', [])[:5]}")

def test_stats():
    """Test the statistics endpoint"""
    print("\n=== Testing /api/stats (all locations) ===")
    response = requests.get(f"{BASE_URL}/api/stats")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(json.dumps(data, indent=2))
    
    print("\n=== Testing /api/stats (Albury only) ===")
    response = requests.get(f"{BASE_URL}/api/stats?location=Albury")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(json.dumps(data, indent=2))

def test_weather_data():
    """Test the weather data endpoint"""
    print("\n=== Testing /api/weather (first 5 records) ===")
    response = requests.get(f"{BASE_URL}/api/weather?limit=5")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total records: {data.get('total')}")
    print(f"Returned: {data.get('count')}")
    print(f"First record: {json.dumps(data.get('data', [])[0] if data.get('data') else {}, indent=2)}")
    
    print("\n=== Testing /api/weather (Albury, high temps) ===")
    response = requests.get(f"{BASE_URL}/api/weather?location=Albury&max_temp_min=30&limit=5")
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Total matching records: {data.get('total')}")
    print(f"Returned: {data.get('count')}")
    if data.get('data'):
        for record in data['data'][:3]:
            print(f"  - Location: {record.get('location')}, Max Temp: {record.get('max_temp')}")

if __name__ == '__main__':
    try:
        print("Testing Weather API Endpoints")
        print("=" * 50)
        
        test_locations()
        test_stats()
        test_weather_data()
        
        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to Flask server.")
        print("Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
