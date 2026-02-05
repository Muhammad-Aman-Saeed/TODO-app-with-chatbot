#!/usr/bin/env python3
"""Debug script to run the server and see any errors"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.main import app
    print("Successfully imported app from backend.main")
    
    import uvicorn
    print("Successfully imported uvicorn")
    
    print("Attempting to run server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    
except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()