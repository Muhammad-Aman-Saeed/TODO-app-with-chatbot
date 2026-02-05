# API Contract: Chat Endpoint

## Endpoint: POST /api/chat

### Description
Endpoint for interacting with the AI chatbot to manage user tasks through natural language.

### Authentication
JWT Bearer token required in Authorization header. Uses existing authentication mechanism.

### Request Body
```json
{
  "message": "string (required) - User's message to the chatbot",
  "conversation_id": "integer (optional) - ID of existing conversation, null for new conversation"
}
```

### Response Body
```json
{
  "conversation_id": "integer - ID of the conversation (newly created or existing)",
  "response": "string - AI-generated response to the user's message",
  "tool_calls": "array of objects (nullable) - Details of any tools called by the AI, null if no tools were called"
}
```

### Example Request
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": null
}
```

### Example Response
```json
{
  "conversation_id": 123,
  "response": "I've added the task 'buy groceries' for you!",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user-123",
        "title": "buy groceries",
        "description": null
      },
      "result": {
        "task_id": 456,
        "status": "created",
        "title": "buy groceries"
      }
    }
  ]
}
```

### Error Responses
- 401: Unauthorized - Invalid or missing JWT token
- 403: Forbidden - User attempting to access another user's conversation
- 422: Unprocessable Entity - Invalid request body format
- 500: Internal Server Error - Issue with AI service or database

### Security Considerations
- Validates that user_id in JWT matches the user_id associated with any referenced conversation
- Sanitizes all user inputs before processing
- Implements rate limiting to prevent abuse