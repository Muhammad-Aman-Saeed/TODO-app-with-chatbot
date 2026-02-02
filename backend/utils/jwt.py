import jwt
from datetime import datetime
from fastapi import HTTPException, status
from typing import Dict, Any
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get the secret key from environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload as dictionary
        
    Raises:
        HTTPException: If token is invalid, expired, or malformed
    """
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract user_id from 'sub' claim (standard JWT claim) or 'user_id' if available
        user_id = payload.get("sub")
        if not user_id:
            user_id = payload.get("user_id")
        
        # Check if user_id exists in the payload
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: user_id not found in payload"
            )
        
        # Check if token has expired
        exp = payload.get("exp")
        if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        
        # Return the payload with user_id
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except jwt.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token signature"
        )
    
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )