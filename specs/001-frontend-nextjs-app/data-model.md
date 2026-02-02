# Data Model: Frontend Next.js Application

## Overview
This document defines the data structures and entities for the frontend Next.js application, based on the feature specification.

## Key Entities

### User
Represents an authenticated user in the system.

**Fields:**
- id: string (unique identifier)
- email: string (user's email address, required, unique)
- name: string (optional, user's display name)
- createdAt: Date (timestamp when user account was created)
- updatedAt: Date (timestamp when user account was last updated)

**Validation Rules:**
- Email must be a valid email format
- Email must be unique across all users
- Name must be 1-50 characters if provided

### Task
Represents a user's task with properties such as title, description, completion status, and creation date.

**Fields:**
- id: string (unique identifier)
- userId: string (foreign key linking to User)
- title: string (task title, required, 1-100 characters)
- description: string (optional, task description, max 1000 characters)
- completed: boolean (task completion status, default: false)
- createdAt: Date (timestamp when task was created)
- updatedAt: Date (timestamp when task was last updated)
- dueDate: Date (optional, deadline for the task)

**Validation Rules:**
- Title must be 1-100 characters
- Description must be 0-1000 characters if provided
- Completed must be a boolean value
- Due date must be a valid date if provided
- Task must belong to a valid user

### Authentication Token
Secure JWT token used for API authentication and authorization.

**Fields:**
- token: string (the JWT token string)
- expiry: Date (timestamp when the token expires)
- type: string (token type, typically "Bearer")

**Validation Rules:**
- Token must be a valid JWT format
- Expiry must be a future date
- Type must be "Bearer"

## State Transitions

### Task State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

### Authentication State Transitions
- `unauthenticated` → `authenticated`: After successful login
- `authenticated` → `unauthenticated`: After logout or token expiration

## Relationships
- User (1) → Task (Many): One user can have many tasks
- Task (Many) → User (1): Many tasks belong to one user

## API Response Structures

### User Response
```typescript
{
  id: string,
  email: string,
  name?: string,
  createdAt: string, // ISO date string
  updatedAt: string  // ISO date string
}
```

### Task Response
```typescript
{
  id: string,
  userId: string,
  title: string,
  description?: string,
  completed: boolean,
  createdAt: string, // ISO date string
  updatedAt: string, // ISO date string
  dueDate?: string   // ISO date string, optional
}
```

### Authentication Response
```typescript
{
  token: string,
  expiry: string, // ISO date string
  type: string,
  user: {
    id: string,
    email: string,
    name?: string
  }
}
```

## Frontend State Models

### Current User State
```typescript
interface CurrentUserState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
```

### Tasks State
```typescript
interface TasksState {
  tasks: Task[];
  filteredTasks: Task[];
  activeFilter: 'all' | 'pending' | 'completed';
  isLoading: boolean;
  error: string | null;
}
```

### UI State
```typescript
interface UIState {
  darkMode: boolean;
  showAddTaskModal: boolean;
  showTaskDetailModal: boolean;
  notifications: Notification[];
}
```