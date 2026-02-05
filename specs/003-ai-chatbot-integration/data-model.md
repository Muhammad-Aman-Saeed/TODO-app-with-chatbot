# Data Model: AI Todo Chatbot Integration

## Overview
This document defines the data models required for the AI Todo Chatbot Integration feature, including entity relationships and validation rules.

## Entity: Conversation
**Description**: Represents a chat session between a user and the AI assistant
**Fields**:
- id: Integer (Primary Key, Auto-increment)
- user_id: String (Foreign Key to user, required)
- title: String (Optional, max 200 characters)
- created_at: DateTime (Required, default to current timestamp)
- updated_at: DateTime (Required, updated on modification)

**Validation Rules**:
- user_id must match an existing authenticated user
- created_at and updated_at are automatically managed by the system

**Relationships**:
- One-to-many with Message entity (one Conversation has many Messages)
- Belongs to a User (via user_id foreign key)

## Entity: Message
**Description**: Represents individual messages within a conversation
**Fields**:
- id: Integer (Primary Key, Auto-increment)
- conversation_id: Integer (Foreign Key to Conversation, required)
- role: String (Literal["user", "assistant"], required)
- content: String (Text content of the message, required)
- created_at: DateTime (Required, default to current timestamp)

**Validation Rules**:
- conversation_id must reference an existing Conversation
- role must be either "user" or "assistant"
- content must not exceed 10,000 characters

**Relationships**:
- Many-to-one with Conversation entity (many Messages belong to one Conversation)

## Entity Relationship Diagram
```
User ||--o{ Conversation }o--o{ Message
```

## State Transitions
- Conversation: Created when first message is sent, updated when new messages are added
- Message: Immutable once created (no state transitions)

## Indexes
- Conversation: Index on user_id for efficient user-specific queries
- Message: Index on conversation_id for efficient conversation retrieval
- Message: Index on created_at for chronological ordering