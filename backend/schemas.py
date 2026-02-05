from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreateRequest(BaseModel):
    """
    Schema for creating a new user
    """
    email: str
    password: str
    name: Optional[str] = None


class UserResponse(BaseModel):
    """
    Schema for returning user data
    """
    id: str
    email: str
    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class TaskCreateRequest(BaseModel):
    """
    Schema for creating a new task
    """
    title: str
    description: Optional[str] = None


class TaskResponse(BaseModel):
    """
    Schema for returning task data
    """
    id: int
    title: str
    description: Optional[str]
    completed: bool
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskUpdateRequest(BaseModel):
    """
    Schema for updating a task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPatchRequest(BaseModel):
    """
    Schema for patching a task (toggling completion)
    """
    completed: bool


class AuthResponse(BaseModel):
    """
    Schema for authentication responses
    """
    user: UserResponse
    token: str