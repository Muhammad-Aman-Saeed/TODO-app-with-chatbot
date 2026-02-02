from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional


class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    user_id: str = Field(min_length=1)


def get_current_time():
    return datetime.now(timezone.utc)


class Task(TaskBase, table=True):
    """
    Task model representing a user's to-do item
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=get_current_time)
    updated_at: Optional[datetime] = Field(default_factory=get_current_time)