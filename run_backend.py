import sys
import os
import logging
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# Now import and run the backend
try:
    from backend.main import app
    import uvicorn

    if __name__ == "__main__":
        # Run with single worker to see errors in the same process
        uvicorn.run(app, host="127.0.0.1", port=8000, workers=1, log_level="debug")
except Exception as e:
    print(f"Error importing or running app: {e}")
    import traceback
    traceback.print_exc()