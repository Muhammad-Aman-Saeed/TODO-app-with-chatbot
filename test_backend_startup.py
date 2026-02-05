"""
Simple test to check if the backend starts properly and the chat endpoint is accessible.
"""
import sys
import os
import subprocess
import time
import requests
import threading

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_backend_startup():
    """Test if the backend starts properly"""
    print("Testing backend startup...")
    
    # Try to start the backend server in a subprocess
    try:
        # Start the server in a subprocess
        proc = subprocess.Popen([
            sys.executable, "-c", 
            "from backend.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give the server some time to start
        time.sleep(3)
        
        # Check if the process is still running
        if proc.poll() is not None:
            # Server failed to start, get the error
            _, stderr = proc.communicate()
            print(f"Server failed to start. Error: {stderr.decode()}")
            return False
        
        print("Backend server appears to be running...")
        
        # Test the health endpoint
        try:
            response = requests.get("http://127.0.0.1:8000/health")
            if response.status_code == 200:
                print("Health check passed!")
            else:
                print(f"Health check failed with status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Could not connect to health endpoint")
        
        # Terminate the server process
        proc.terminate()
        proc.wait()
        
        return True
        
    except Exception as e:
        print(f"Error starting backend: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_dependencies():
    """Test if all required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "uvicorn"),
        ("sqlmodel", "SQLModel"),
        ("cohere", "cohere"),
        ("jwt", "jwt"),
        ("dotenv", "load_dotenv"),
    ]
    
    for module_name, import_as in dependencies:
        try:
            if module_name == "dotenv":
                from dotenv import load_dotenv
            elif module_name == "jwt":
                import jwt
            elif module_name == "cohere":
                import cohere
            elif module_name == "fastapi":
                from fastapi import FastAPI
            elif module_name == "uvicorn":
                import uvicorn
            elif module_name == "sqlmodel":
                from sqlmodel import SQLModel
            print(f"[OK] {module_name} is available")
        except ImportError as e:
            print(f"[ERROR] {module_name} is NOT available: {e}")


def check_routes():
    """Check if the chat route is properly defined"""
    print("\nChecking routes...")
    
    try:
        from backend.main import app
        route_names = [route.name for route in app.routes]
        print(f"Available routes: {route_names}")
        
        # Check if chat endpoint is available
        chat_routes = [route for route in app.routes if "/api/chat" in str(route.path)]
        if chat_routes:
            print("[OK] Chat endpoint is available")
        else:
            print("[ERROR] Chat endpoint is NOT available")
            
    except Exception as e:
        print(f"Error checking routes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("Backend Functionality Diagnostic Tool\n")
    print("="*50)
    
    test_dependencies()
    check_routes()
    test_backend_startup()
    
    print("\n" + "="*50)
    print("Diagnostic complete.")
    print("\nThe most likely issue is that the chatbot requires a valid JWT token to function.")
    print("Make sure you're sending the Authorization header with a valid Bearer token.")
    print("Also, ensure you have a valid Cohere API key in your .env file for full functionality.")