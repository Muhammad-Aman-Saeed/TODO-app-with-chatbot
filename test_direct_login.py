import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Directly test the login function
print("Testing login function directly...")

try:
    # Import the login function
    from backend.routes.debug_auth import login, LoginRequest
    
    # Create a test request
    login_request = LoginRequest(email="test@example.com", password="password")
    
    print("Calling login function...")
    result = login(login_request)
    
    print(f"Login function succeeded: {result}")
    
except Exception as e:
    print(f"Error in login function: {e}")
    import traceback
    traceback.print_exc()