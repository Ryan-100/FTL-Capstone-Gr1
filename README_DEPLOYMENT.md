# Deployment Guide for HuggingFace Spaces

This guide explains how to deploy the Disease Outbreak Prediction API to HuggingFace Spaces using Docker.

## Prerequisites

1. A HuggingFace account
2. Docker installed locally (for testing)
3. All required files in the repository

## Files Required for Deployment

Make sure these files are in your repository:
- `Dockerfile`
- `requirements.txt`
- `api/main.py`
- `api/static/` (all UI files)
- `models/lstm_best_model.keras`
- `data/japan_covid_master_data.csv`

## Deployment Steps

### 1. Create a HuggingFace Space

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `disease-outbreak-prediction` (or your preferred name)
   - **SDK**: Select **Docker**
   - **Hardware**: Choose based on your needs (CPU Basic is usually sufficient)
   - **Visibility**: Public or Private

### 2. Upload Files

You can upload files in two ways:

#### Option A: Using Git (Recommended)
```bash
# Clone your HuggingFace Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy all necessary files
cp Dockerfile .
cp requirements.txt .
cp -r api/ .
cp -r models/ .
cp -r data/ .

# Commit and push
git add .
git commit -m "Add Docker deployment files"
git push
```

#### Option B: Using Web Interface
1. Go to your Space page
2. Click "Files and versions" tab
3. Upload files using the web interface

### 3. Required Files Structure

Your Space should have this structure:
```
.
├── Dockerfile
├── requirements.txt
├── api/
│   ├── __init__.py
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── script.js
├── models/
│   └── lstm_best_model.keras
└── data/
    └── japan_covid_master_data.csv
```

### 4. Build and Deploy

HuggingFace Spaces will automatically:
1. Build the Docker image using the Dockerfile
2. Start the container
3. Make your app available at: `https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space`

## Testing Locally

Before deploying, test the Docker container locally:

```bash
# Build the image
docker build -t disease-prediction-api .

# Run the container
docker run -p 7860:7860 disease-prediction-api

# Test in browser
# Open http://localhost:7860
```

## Environment Variables

The application uses the `PORT` environment variable (defaults to 7860 for HuggingFace Spaces).

## Troubleshooting

### Build Fails
- Check that all required files are present
- Verify the Dockerfile paths are correct
- Check the logs in HuggingFace Spaces

### Model Not Loading
- Ensure `models/lstm_best_model.keras` is uploaded
- Check file size limits (HuggingFace Spaces has limits)
- Verify the model path in `api/main.py`

### Data File Not Found
- Ensure `data/japan_covid_master_data.csv` is uploaded
- Check the file path in `api/main.py`

### Port Issues
- HuggingFace Spaces uses port 7860 by default
- The Dockerfile is configured to use port 7860
- If using a different port, update both Dockerfile and CMD

## Resources

- [HuggingFace Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Docker Documentation](https://docs.docker.com/)

## Notes

- The first build may take 10-15 minutes (downloading dependencies and model)
- Subsequent builds are faster due to caching
- Free tier has resource limits - consider upgrading for production use
- Model file size: Make sure your model file is within HuggingFace Spaces limits

