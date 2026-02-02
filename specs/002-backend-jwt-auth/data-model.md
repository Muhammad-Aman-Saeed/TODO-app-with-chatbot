# Data Model: Backend JWT Authentication Implementation

## Entity: Task
**Description**: Represents a user's to-do item with properties like title, description, completion status, and association to a user

**Fields**:
- id (Integer, Primary Key, Auto-generated): Unique identifier for the task
- title (String, Required): The title or name of the task
- description (String, Optional): Detailed description of the task
- completed (Boolean, Default: False): Status indicating if the task is completed
- user_id (String, Required, Foreign Key): Reference to the user who owns this task
- created_at (DateTime, Optional, Default: now): Timestamp when the task was created
- updated_at (DateTime, Optional, Default: now): Timestamp when the task was last updated

**Validation Rules**:
- title must not be empty
- user_id must match the authenticated user's ID
- completed must be a boolean value

**Relationships**:
- Belongs to a User (many-to-one relationship through user_id foreign key)

**State Transitions**:
- created → pending (initial state when task is created)
- pending → completed (when task is marked as done)
- completed → pending (when task is unmarked as done)

## Entity: User (Reference)
**Description**: Represents an authenticated user identified by user_id extracted from JWT token

**Fields**:
- id (String, Primary Key): Unique identifier for the user (extracted from JWT)

**Note**: The User entity is managed by Better Auth and referenced via foreign key in the Task entity. We don't need to define this model in SQLModel as it's handled by the authentication system.