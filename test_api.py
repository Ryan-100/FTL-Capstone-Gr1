"""
Simple test script for the Disease Outbreak Prediction API
Run this after starting the API server
"""
import requests
import json

# API endpoint
url = "http://localhost:8000/predict"

# Example data: 30 days of new_cases
# You can replace this with actual historical data
test_data = {
    "new_cases": [
        100, 120, 150, 180, 200, 220, 240, 260, 280, 300,
        320, 340, 360, 380, 400, 420, 440, 460, 480, 500,
        520, 540, 560, 580, 600, 620, 640, 660, 680, 700
    ]
}

def test_api():
    """Test the prediction API"""
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        health_response = requests.get("http://localhost:8000/health")
        print(f"Health Status: {health_response.json()}\n")
        
        # Test prediction endpoint
        print("Testing prediction endpoint...")
        print(f"Sending request with {len(test_data['new_cases'])} days of data...")
        
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Prediction successful!")
            print(f"Predicted new cases for next day: {result['predicted_cases']:.2f}")
            print(f"Message: {result['message']}")
        else:
            print(f"\n❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the API server is running on http://localhost:8000")
        print("\nStart the server with:")
        print("  uvicorn api.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_api()

