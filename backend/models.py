from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Index
from passlib.context import CryptContext


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)


class User(UserBase, table=True):
    """
    User model representing application users
    """
    id: Optional[str] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True, min_length=1)  # Add index for better performance


def get_current_time():
    return datetime.now(timezone.utc)


class Task(TaskBase, table=True):
    """
    Task model representing a user's to-do item
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=get_current_time)
    updated_at: Optional[datetime] = Field(default_factory=get_current_time)


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session between a user and the AI assistant
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)  # Foreign Key to user, with index for performance
    title: Optional[str] = Field(default=None, max_length=200)  # Optional title
    created_at: Optional[datetime] = Field(default_factory=get_current_time, index=True)
    updated_at: Optional[datetime] = Field(default_factory=get_current_time)


class Message(SQLModel, table=True):
    """
    Message model representing individual messages within a conversation
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)  # Foreign Key to Conversation, with index
    role: str = Field(sa_column_kwargs={"default": "user"})  # "user" or "assistant"
    content: str = Field(max_length=10000)  # Text content of the message
    created_at: Optional[datetime] = Field(default_factory=get_current_time, index=True)  # Index for chronological ordering


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain password"""
    return pwd_context.hash(password)