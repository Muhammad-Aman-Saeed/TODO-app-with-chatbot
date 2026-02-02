import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test importing the main components individually
print("Testing individual imports...")

try:
    print("1. Importing FastAPI components...")
    from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
    print("   OK FastAPI components imported successfully")
except Exception as e:
    print(f"   ERROR importing FastAPI components: {e}")

try:
    print("2. Importing datetime components...")
    from datetime import datetime, timedelta, timezone
    print("   OK Datetime components imported successfully")
except Exception as e:
    print(f"   ERROR importing datetime components: {e}")

try:
    print("3. Importing JWT...")
    import jwt
    print("   OK JWT imported successfully")
except Exception as e:
    print(f"   ERROR importing JWT: {e}")

try:
    print("4. Importing SQLModel...")
    from sqlmodel import SQLModel, Field, create_engine, Session
    print("   OK SQLModel imported successfully")
except Exception as e:
    print(f"   ERROR importing SQLModel: {e}")

try:
    print("5. Importing models...")
    from backend.models import Task
    print("   OK Models imported successfully")
except Exception as e:
    print(f"   ERROR importing models: {e}")

try:
    print("6. Importing routes...")
    from backend.routes.tasks import router as tasks_router
    print("   OK Tasks route imported successfully")
except Exception as e:
    print(f"   ERROR importing tasks route: {e}")

try:
    print("7. Importing simple auth route...")
    from backend.routes.simple_auth import router as auth_router
    print("   OK Simple auth route imported successfully")
except Exception as e:
    print(f"   ERROR importing simple auth route: {e}")

try:
    print("8. Importing dependencies...")
    from backend.dependencies import get_current_user, get_db_session
    print("   OK Dependencies imported successfully")
except Exception as e:
    print(f"   ERROR importing dependencies: {e}")

print("\nAll imports tested!")