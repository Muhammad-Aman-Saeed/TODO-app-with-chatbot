# Quickstart Guide: Backend JWT Authentication Implementation

## Prerequisites
- Python 3.9+
- pip package manager
- Access to Neon PostgreSQL database
- Better Auth configured on the frontend

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hackathon-todo
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the backend directory with the following:
   ```
   DATABASE_URL=postgresql://username:password@neon-host/db-name
   BETTER_AUTH_SECRET=zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5
   ```

6. **Run the application**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## API Usage

Once the server is running, you can access the API at `http://localhost:8000`.

### Authentication
All endpoints require a valid JWT token from Better Auth in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

### Available Endpoints

#### GET /api/tasks
Retrieve all tasks for the authenticated user.
Query parameters:
- `status`: Filter by status (all|pending|completed)
- `sort`: Sort by (created|title)

#### POST /api/tasks
Create a new task.
Body:
```json
{
  "title": "Task title",
  "description": "Task description (optional)"
}
```

#### GET /api/tasks/{id}
Get a specific task by ID.

#### PUT /api/tasks/{id}
Update a specific task.
Body:
```json
{
  "title": "Updated title (optional)",
  "description": "Updated description (optional)",
  "completed": true (optional)
}
```

#### DELETE /api/tasks/{id}
Delete a specific task.

#### PATCH /api/tasks/{id}/complete
Toggle the completion status of a specific task.

## Testing the API

You can test the API using curl or a tool like Postman:

```bash
curl -X GET \
  http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <valid-jwt-token>"
```

## Troubleshooting

- If you get a 401 error, ensure your JWT token is valid and not expired
- If you get a 403 error, verify that you're only accessing tasks that belong to your user
- Check the logs for any database connection issues