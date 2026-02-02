from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from ..dependencies import get_current_user
from ..schemas import TaskResponse

# Load environment variables
load_dotenv()

# Get the secret key from environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class AuthResponse(BaseModel):
    user: dict  # Simplified - in real implementation, use proper User model
    token: str


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a new JWT access token

    Args:
        data: Dictionary with the data to encode in the token
        expires_delta: Optional timedelta for token expiration

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login", response_model=AuthResponse)
def login(login_data: LoginRequest):
    """
    Login endpoint - in a real implementation, this would verify credentials
    For now, we'll simulate successful login and return a proper JWT token
    """
    # In a real implementation, you would verify the email/password against the database
    # Here we're simulating successful login

    # Create a JWT token with user information
    user_data = {
        "id": f"user-{abs(hash(login_data.email)) % 10000}",  # Generate a unique ID based on email
        "email": login_data.email,
        "name": "User"  # LoginRequest doesn't have a name field, so default to "User"
    }

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user_data["id"],  # Using 'sub' as the standard JWT claim for user ID
        "user_id": user_data["id"],
        "email": user_data["email"]
    }
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    return AuthResponse(user=user_data, token=token)


@router.post("/register", response_model=AuthResponse)
def register(register_data: RegisterRequest):
    """
    Register endpoint - in a real implementation, this would create a new user
    For now, we'll simulate successful registration and return a proper JWT token
    """
    # In a real implementation, you would create a new user in the database
    # Here we're simulating successful registration

    # Create a JWT token with user information
    user_data = {
        "id": f"user-{hash(register_data.email) % 10000}",  # Generate a unique ID based on email
        "email": register_data.email,
        "name": register_data.name or "User"
    }

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user_data["id"],  # Using 'sub' as the standard JWT claim for user ID
        "user_id": user_data["id"],
        "email": user_data["email"]
    }
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    return AuthResponse(user=user_data, token=token)


@router.get("/token")
def get_auth_token(current_user_id: str = Depends(get_current_user)):
    """
    Get auth token endpoint - returns token information for the current user
    """
    # This endpoint requires authentication, so the user is already validated
    # In a real implementation, you might refresh or return token details
    # For now, we'll return dummy data

    return {
        "user_id": current_user_id,
        "expiresAt": (datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat().replace('+00:00', 'Z')
    }