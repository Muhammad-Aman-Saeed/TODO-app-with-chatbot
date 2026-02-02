import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test JWT functionality separately
from datetime import datetime, timezone
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"

def create_test_token():
    """Test creating a JWT token"""
    data = {
        "sub": "user-123",
        "user_id": "user-123",
        "email": "test@example.com"
    }
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    data.update({"exp": expire})
    
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Created token: {encoded_jwt}")
    
    # Test decoding
    decoded = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded token: {decoded}")
    
    return encoded_jwt

if __name__ == "__main__":
    from datetime import timedelta
    print("Testing JWT functionality...")
    token = create_test_token()
    print("JWT test completed successfully!")