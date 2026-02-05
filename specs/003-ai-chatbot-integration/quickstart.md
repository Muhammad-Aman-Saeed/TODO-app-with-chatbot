# Quickstart Guide: AI Todo Chatbot Integration

## Overview
This guide provides a quick walkthrough of the AI Todo Chatbot Integration feature implementation.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Cohere API key
- Existing project setup from Phase II

## Setup Instructions

### 1. Install Backend Dependencies
```bash
pip install cohere
```

### 2. Update Environment Variables
Add to your `.env` file:
```
COHERE_API_KEY=your_cohere_api_key_here
```

### 3. Update Database Models
Add Conversation and Message models to your existing models.py file with the required fields and relationships.

### 4. Create Tool Definitions
Define the 5 required tools (add_task, list_tasks, complete_task, delete_task, get_user_info) with proper JSON schemas for Cohere.

### 5. Implement Service Layer
Create service functions that execute the tools with proper user validation against the authenticated user.

### 6. Create Chat Endpoint
Implement the POST /api/chat endpoint with JWT authentication, conversation management, and Cohere integration.

### 7. Handle Tool Execution Loop
Implement the logic to handle multiple tool calls in sequence and feed results back to Cohere.

### 8. Create Frontend Components
- Create ChatbotIcon component for the floating chat button
- Create ChatModal component for the chat interface
- Update dashboard to include the chatbot icon

### 9. Update API Client
Add a chat() method to your existing API client with proper JWT header handling.

## Running the Feature

### Backend
1. Ensure your database is migrated with the new Conversation and Message tables
2. Start your FastAPI server
3. The /api/chat endpoint should be available

### Frontend
1. The chatbot icon should appear in the bottom-right of the dashboard
2. Clicking the icon should open the chat modal
3. Users can interact with the AI to manage their tasks

## Testing
1. Test the API endpoint directly with curl or Postman
2. Test the frontend integration
3. Verify user isolation (users can only access their own conversations)
4. Test all 5 tools through the chat interface

## Troubleshooting
- If Cohere API calls fail, verify your API key in the environment variables
- If authentication fails, ensure JWT tokens are properly passed
- If conversations don't persist, check database connectivity and model relationships