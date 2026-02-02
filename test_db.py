import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test database connection
from backend.db import engine

try:
    print("Testing database engine creation...")
    print(f"Engine created: {engine}")
    
    # Try to connect
    with engine.connect() as conn:
        print("Database connection successful!")
        result = conn.execute("SELECT 1")
        print(f"Query result: {result.fetchone()}")
        
except Exception as e:
    print(f"Database connection failed: {e}")
    import traceback
    traceback.print_exc()