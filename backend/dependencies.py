from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session
from .db import get_session
from .utils.jwt import verify_token
from typing import Dict, Any, Optional
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def get_current_user(request: Request) -> str:
    """
    Dependency to get the current user from JWT token
    
    Args:
        request: FastAPI request object
        
    Returns:
        User ID string from the JWT token
        
    Raises:
        HTTPException: If no valid token is provided or token is invalid
    """
    # Get the authorization header
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Extract the token from the header
    token = auth_header.split(" ")[1]
    
    # Verify the token and get the payload
    try:
        payload = verify_token(token)
    except HTTPException:
        # Re-raise the HTTPException from verify_token
        raise
    
    # Extract user_id from the payload
    user_id = payload.get("sub") or payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user_id not found in payload"
        )
    
    return user_id


def get_db_session():
    """
    Dependency to get a database session
    """
    yield next(get_session())