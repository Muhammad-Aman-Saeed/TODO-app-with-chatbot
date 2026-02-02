# API Contracts: Frontend Next.js Application

## Overview
This document defines the API contracts between the frontend Next.js application and the backend API at http://localhost:8000/api.

## Authentication Endpoints

### POST /api/auth/register
Register a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": "user_123456789",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-02-01T10:00:00.000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid input",
  "details": ["Email is required", "Password must be at least 8 characters"]
}
```

### POST /api/auth/login
Authenticate a user and return JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": "user_123456789",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-02-01T10:00:00.000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

### GET /api/auth/token
Get a fresh JWT token for authenticated user (requires session cookie).

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-02-01T11:00:00.000Z"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

## Task Management Endpoints

### GET /api/tasks
Retrieve all tasks for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
[
  {
    "id": "task_123456789",
    "userId": "user_123456789",
    "title": "Complete project proposal",
    "description": "Finish the project proposal document and send to team",
    "completed": false,
    "createdAt": "2026-02-01T09:00:00.000Z",
    "updatedAt": "2026-02-01T09:00:00.000Z",
    "dueDate": "2026-02-05T00:00:00.000Z"
  },
  {
    "id": "task_987654321",
    "userId": "user_123456789",
    "title": "Schedule team meeting",
    "description": "Arrange meeting with team for project kickoff",
    "completed": true,
    "createdAt": "2026-02-01T08:00:00.000Z",
    "updatedAt": "2026-02-01T08:30:00.000Z",
    "dueDate": null
  }
]
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

### POST /api/tasks
Create a new task for the authenticated user.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "title": "Prepare presentation",
  "description": "Create slides for quarterly review",
  "dueDate": "2026-02-10T00:00:00.000Z"
}
```

**Response (201 Created):**
```json
{
  "id": "task_111222333",
  "userId": "user_123456789",
  "title": "Prepare presentation",
  "description": "Create slides for quarterly review",
  "completed": false,
  "createdAt": "2026-02-01T10:30:00.000Z",
  "updatedAt": "2026-02-01T10:30:00.000Z",
  "dueDate": "2026-02-10T00:00:00.000Z"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Validation failed",
  "details": ["Title is required", "Due date must be in the future"]
}
```

### PUT /api/tasks/{taskId}
Update an existing task.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "title": "Updated presentation title",
  "description": "Create slides for quarterly review - updated",
  "completed": false,
  "dueDate": "2026-02-12T00:00:00.000Z"
}
```

**Response (200 OK):**
```json
{
  "id": "task_111222333",
  "userId": "user_123456789",
  "title": "Updated presentation title",
  "description": "Create slides for quarterly review - updated",
  "completed": false,
  "createdAt": "2026-02-01T10:30:00.000Z",
  "updatedAt": "2026-02-01T11:00:00.000Z",
  "dueDate": "2026-02-12T00:00:00.000Z"
}
```

### PATCH /api/tasks/{taskId}/toggle
Toggle the completion status of a task.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": "task_111222333",
  "userId": "user_123456789",
  "title": "Updated presentation title",
  "description": "Create slides for quarterly review - updated",
  "completed": true,
  "createdAt": "2026-02-01T10:30:00.000Z",
  "updatedAt": "2026-02-01T11:15:00.000Z",
  "dueDate": "2026-02-12T00:00:00.000Z"
}
```

### DELETE /api/tasks/{taskId}
Delete a task.

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (204 No Content):**
```
[Empty response body]
```

**Response (404 Not Found):**
```json
{
  "error": "Task not found"
}
```

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Human-readable error message",
  "details": ["Array of specific validation errors if applicable"]
}
```

## Authentication Headers

All authenticated endpoints require the following header:
```
Authorization: Bearer {jwt_token}
```

The JWT token should be obtained via the login endpoint or refreshed via the token endpoint.