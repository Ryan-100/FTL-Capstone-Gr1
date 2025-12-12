# Disease Outbreak Prediction API

FastAPI endpoint for serving the LSTM disease outbreak prediction model.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

### Option 1: Using uvicorn directly
```bash
uvicorn api.main:app --reload
```

### Option 2: Running the main file
```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

## Web UI

A user-friendly web interface is available at the root URL (`http://localhost:8000/`). The UI allows you to:

- **Manual Input**: Enter 30 days of new cases data directly in the form
- **Load Sample Data**: Click to populate with sample data for testing
- **Upload CSV**: Upload a CSV file with new_cases column (will use the last 30 values)
- **Make Predictions**: Get instant predictions with a beautiful visual display

The UI features:
- Modern, responsive design
- Real-time input validation
- Loading indicators
- Error handling
- Visual prediction results

## API Endpoints

### 1. Root Endpoint
- **URL**: `GET /`
- **Description**: Returns API information and available endpoints

### 2. Health Check
- **URL**: `GET /health`
- **Description**: Check if the model and scaler are loaded correctly

### 3. Prediction Endpoint
- **URL**: `POST /predict`
- **Description**: Predict new cases for the next day based on 30 days of historical data

**Request Body**:
```json
{
  "new_cases": [100, 120, 150, 180, 200, ...]  // Exactly 30 values
}
```

**Response**:
```json
{
  "predicted_cases": 250.5,
  "message": "Prediction successful"
}
```

## Example Usage

### Using curl:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "new_cases": [100, 120, 150, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520, 540, 560, 580, 600, 620, 640, 660, 680, 700]
  }'
```

### Using Python requests:
```python
import requests

url = "http://localhost:8000/predict"
data = {
    "new_cases": [100, 120, 150, 180, 200, 220, 240, 260, 280, 300, 
                  320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 
                  520, 540, 560, 580, 600, 620, 640, 660, 680, 700]
}

response = requests.post(url, json=data)
print(response.json())
```

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Notes

- The model expects exactly 30 days of `new_cases` data
- The input data is automatically scaled using the same MinMaxScaler used during training
- The prediction is returned in the original scale (not normalized)

