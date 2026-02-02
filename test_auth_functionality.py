import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test the login function in isolation
print("Testing auth functionality...")

try:
    from backend.routes.auth import create_access_token, LoginRequest
    from pydantic import ValidationError
    
    # Test creating a token
    print("Testing token creation...")
    token_data = {
        "sub": "user-123",
        "user_id": "user-123",
        "email": "test@example.com"
    }
    
    token = create_access_token(token_data)
    print(f"Token created successfully: {token[:50]}...")
    
    # Test request model
    print("Testing request model...")
    login_req = LoginRequest(email="test@example.com", password="password")
    print(f"Login request created: {login_req}")
    
    print("Auth functionality test completed successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"Error in auth functionality: {e}")
    import traceback
    traceback.print_exc()