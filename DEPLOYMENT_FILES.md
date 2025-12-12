# Files to Upload to HuggingFace Spaces

When deploying to HuggingFace Spaces, make sure to include these files:

## Required Files

```
.
├── Dockerfile                    # Docker configuration
├── requirements.txt              # Python dependencies
├── app.py                        # Entry point for HuggingFace Spaces
├── api/
│   ├── __init__.py
│   ├── main.py                   # FastAPI application
│   └── static/
│       ├── index.html            # Web UI
│       ├── style.css             # UI styles
│       └── script.js             # UI JavaScript
├── models/
│   └── lstm_best_model.keras    # Trained LSTM model
└── data/
    └── japan_covid_master_data.csv  # Training data (for scaler)
```

## Quick Upload Checklist

- [ ] Dockerfile
- [ ] requirements.txt
- [ ] app.py
- [ ] api/ directory (with all subdirectories)
- [ ] models/lstm_best_model.keras
- [ ] data/japan_covid_master_data.csv

## File Size Notes

- Model file (`lstm_best_model.keras`) can be large
- HuggingFace Spaces free tier has file size limits
- If model is too large, consider using Git LFS or upgrading your plan

## Testing Before Upload

Test locally with Docker:
```bash
docker build -t disease-prediction .
docker run -p 7860:7860 disease-prediction
```

Then visit: http://localhost:7860

