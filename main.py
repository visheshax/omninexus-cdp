import os
import sys

# Ensure the backend folder is in the python path for absolute imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the FastAPI application
from backend.main import app

if __name__ == "__main__":
    import uvicorn
    # Render binds the application to the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
