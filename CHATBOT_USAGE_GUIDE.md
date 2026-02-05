# Chatbot Usage Guide

## Overview
The chatbot is fully functional but requires proper authentication and configuration to work correctly. This guide explains how to use it properly.

## Prerequisites

### 1. Authentication
The chatbot requires a valid JWT token to function. You must authenticate first before using the chatbot.

### 2. API Key (Optional but Recommended)
While the system has mock responses, a Cohere API key provides better AI responses.

## Setup Instructions

### 1. Get a Cohere API Key (Recommended)
1. Visit [Cohere Dashboard](https://dashboard.cohere.ai/api-keys)
2. Create an account or log in
3. Generate a new API key
4. Update your `.env` file:
   ```
   COHERE_API_KEY=your_actual_cohere_api_key_here
   ```

### 2. Authentication Flow
The chatbot requires authentication. Follow these steps:

#### Step 1: Register a User
Send a POST request to `/api/register`:
```json
{
  "email": "your-email@example.com",
  "password": "your-password",
  "name": "Your Name"
}
```

#### Step 2: Login to Get Token
Send a POST request to `/api/login`:
```json
{
  "email": "your-email@example.com",
  "password": "your-password"
}
```

You'll receive a response with an access token:
```json
{
  "user": {...},
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Step 3: Use the Chatbot
Send requests to `/api/chat` with the Authorization header:
```json
{
  "message": "Add a task to clean my room",
  "conversation_id": null
}
```

Headers:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Chatbot Capabilities

### 1. Task Management
- **Add tasks**: "Add a task to clean my room"
- **List tasks**: "Show me my tasks" or "List my tasks"
- **Complete tasks**: "Complete task 1" or "Mark task 1 as done"
- **Delete tasks**: "Delete task 2" or "Remove task 2"
- **Edit tasks**: "Edit task 1 to say 'updated task name'"

### 2. General Conversation
- **Greetings**: "Hello!", "Hi there"
- **Capabilities**: "What can you do?", "How are you?"

## Example Usage

### Using curl:
```bash
# Register
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123", "name": "Test User"}'

# Login
LOGIN_RESPONSE=$(curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}')

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')

# Use the chatbot
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Add a task to clean my room"}'
```

### Using Python requests:
```python
import requests

# Login to get token
login_data = {
    "email": "test@example.com",
    "password": "password123"
}
login_response = requests.post("http://localhost:8000/api/login", json=login_data)
token = login_response.json()["token"]

# Use the chatbot
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
chat_data = {
    "message": "Add a task to clean my room",
    "conversation_id": None
}
chat_response = requests.post("http://localhost:8000/api/chat", json=chat_data, headers=headers)
print(chat_response.json())
```

## Troubleshooting

### Common Issues:

1. **"Not authenticated" error**: Make sure you're sending the Authorization header with a valid Bearer token.

2. **Chatbot not responding**: Ensure you've completed the authentication flow and are using the correct token.

3. **Cohere API not working**: If using mock responses, the bot will still function but with predefined responses. For better AI responses, add a valid Cohere API key.

4. **Database errors**: Make sure the database is properly initialized. The system creates tables automatically on startup.

## Development Mode
In development mode (without a Cohere API key), the system uses enhanced mock responses that provide:
- Natural language processing
- Task management capabilities
- Conversational abilities
- Proper error handling

The mock responses have been enhanced to provide a more natural and engaging experience while maintaining all functionality.