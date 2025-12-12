"""
Entry point for HuggingFace Spaces deployment
This file is required by HuggingFace Spaces to recognize the app
"""
from api.main import app

# HuggingFace Spaces will automatically detect this app instance
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

