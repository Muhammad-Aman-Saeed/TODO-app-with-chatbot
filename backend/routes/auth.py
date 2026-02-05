from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Optional
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from sqlmodel import Session, select

from ..dependencies import get_current_user, get_db_session
from ..models import User, get_password_hash, verify_password
from ..schemas import UserCreateRequest, UserResponse, AuthResponse

# Load environment variables
load_dotenv()

# Get the secret key from environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])

security = HTTPBearer()


from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str


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
def login(login_data: LoginRequest, db: Session = Depends(get_db_session)):
    """
    Login endpoint - verifies credentials against the database
    """
    # Find the user by email
    user = db.exec(select(User).where(User.email == login_data.email)).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.id,  # Using 'sub' as the standard JWT claim for user ID
        "user_id": user.id,
        "email": user.email
    }
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    # Return user data and token
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return AuthResponse(user=user_response, token=token)


@router.post("/register", response_model=AuthResponse)
def register(register_data: UserCreateRequest, db: Session = Depends(get_db_session)):
    """
    Register endpoint - creates a new user in the database
    """
    # Check if user already exists
    existing_user = db.exec(select(User).where(User.email == register_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a new user with hashed password
    user_id = f"user-{abs(hash(register_data.email)) % 1000000}"  # Generate a unique ID based on email
    hashed_password = get_password_hash(register_data.password)

    user = User(
        id=user_id,
        email=register_data.email,
        name=register_data.name,
        hashed_password=hashed_password
    )

    # Add the user to the database
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": user.id,  # Using 'sub' as the standard JWT claim for user ID
        "user_id": user.id,
        "email": user.email
    }
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    # Return user data and token
    user_response = UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return AuthResponse(user=user_response, token=token)


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