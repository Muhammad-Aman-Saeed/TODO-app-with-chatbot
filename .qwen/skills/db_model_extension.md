# DB Model Extension

## Description
Add Conversation & Message models to the database schema using SQLModel.

## Output Format
```python
# backend/models.py additions

from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Conversation(SQLModel, table=True):
    """
    Represents a conversation between a user and the assistant.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # Reference to the authenticated user
    title: str = Field(max_length=255)  # Auto-generated or user-defined title
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship to messages in this conversation
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Represents a message within a conversation.
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    role: str = Field(max_length=20)  # 'user', 'assistant', 'system'
    content: str  # The actual message content
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[str] = Field(default=None)  # Optional JSON string for additional data
    
    # Relationship back to the conversation
    conversation: Conversation = Relationship(back_populates="messages")
```

## Implementation Notes
- Both models inherit from SQLModel and have table=True to create database tables
- Use UUID for primary keys to ensure global uniqueness
- Include proper indexing on foreign keys and commonly queried fields
- Add relationships between models to enable easy querying
- Include timestamps for audit trails
- Consider adding indexes for performance optimization based on query patterns