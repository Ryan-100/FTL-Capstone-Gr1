"""
FastAPI endpoint for Disease Outbreak Prediction using LSTM model
"""
import os
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Initialize FastAPI app
app = FastAPI(
    title="Disease Outbreak Prediction API",
    description="API for predicting disease outbreak cases using LSTM model",
    version="1.0.0"
)

# Global variables for model and scaler
model = None
scaler = None
WINDOW_SIZE = 30

class PredictionRequest(BaseModel):
    """Request model for prediction endpoint"""
    new_cases: List[float] = Field(
        ...,
        description="List of 30 consecutive days of new_cases values",
        min_length=WINDOW_SIZE,
        max_length=WINDOW_SIZE
    )

class PredictionResponse(BaseModel):
    """Response model for prediction endpoint"""
    predicted_cases: float = Field(..., description="Predicted new cases for the next day")
    message: str = Field(..., description="Status message")

def load_model_and_scaler():
    """Load the trained model and initialize scaler from training data"""
    global model, scaler
    
    # Get the base directory (parent of 'api' folder)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models", "lstm_best_model.keras")
    data_path = os.path.join(base_dir, "data", "japan_covid_master_data.csv")
    
    # Load the model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
    
    print(f"Loading model from {model_path}...")
    model = load_model(model_path)
    print("Model loaded successfully!")
    
    # Load data and fit scaler (same as training)
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    print(f"Loading data from {data_path} to initialize scaler...")
    df = pd.read_csv(data_path).ffill()  # Using ffill() instead of deprecated fillna(method='ffill')
    data = df['new_cases'].values.reshape(-1, 1)
    
    # Initialize and fit scaler (same as training)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler.fit(data)
    print("Scaler initialized successfully!")

@app.on_event("startup")
async def startup_event():
    """Load model and scaler when the API starts"""
    try:
        load_model_and_scaler()
    except Exception as e:
        print(f"Error during startup: {str(e)}")
        raise

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def root():
    """Serve the UI"""
    ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "index.html")
    if os.path.exists(ui_path):
        return FileResponse(ui_path)
    return {
        "message": "Disease Outbreak Prediction API",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Make predictions (requires 30 days of new_cases data)",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict new cases for the next day based on 30 days of historical data
    
    Args:
        request: PredictionRequest containing 30 days of new_cases values
    
    Returns:
        PredictionResponse with predicted cases for the next day
    """
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model or scaler not loaded. Please check server logs."
        )
    
    try:
        # Convert input to numpy array
        input_data = np.array(request.new_cases)
        
        # Reshape for scaler (needs 2D array)
        input_data_2d = input_data.reshape(-1, 1)
        
        # Scale the input data
        input_scaled = scaler.transform(input_data_2d)
        
        # Reshape for LSTM model: (1, window_size, 1)
        input_reshaped = input_scaled.reshape(1, WINDOW_SIZE, 1)
        
        # Make prediction
        prediction_scaled = model.predict(input_reshaped, verbose=0)
        
        # Inverse transform to get actual value
        prediction_actual = scaler.inverse_transform(prediction_scaled)
        
        # Extract the predicted value
        predicted_cases = float(prediction_actual[0, 0])
        
        return PredictionResponse(
            predicted_cases=predicted_cases,
            message="Prediction successful"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error making prediction: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    import os
    # Use PORT environment variable if available (for HuggingFace Spaces), otherwise default to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

