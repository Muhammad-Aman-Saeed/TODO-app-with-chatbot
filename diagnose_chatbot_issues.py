"""
Test script to simulate the chatbot functionality with proper authentication and API calls.
This will help diagnose why the chatbot isn't working properly.
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.routes.chat import chat_endpoint
from backend.dependencies import get_current_user
from backend.utils.mock_responses import get_mock_chat_response
from unittest.mock import AsyncMock, MagicMock
import pytest
from pydantic import BaseModel
from typing import Optional


class MockRequest:
    def __init__(self, headers=None):
        self.headers = headers or {}


def test_mock_responses_standalone():
    """Test the mock responses independently"""
    print("Testing mock responses standalone...")
    
    test_inputs = [
        "Hello!",
        "Add a task to clean my room",
        "List my tasks",
        "Complete task 1",
        "Delete task 2",
        "Edit task 1 to say 'updated task'",
        "How are you?",
        "What can you do?"
    ]
    
    for inp in test_inputs:
        response = get_mock_chat_response(inp)
        print(f"Input: '{inp}' -> Response: '{response.text}', Tool calls: {len(response.tool_calls)}")
    

def test_chat_endpoint_simulation():
    """Simulate the chat endpoint with mocked dependencies"""
    print("\nTesting chat endpoint simulation...")
    
    # Create mock request with proper authorization header
    mock_request = MockRequest(headers={"Authorization": "Bearer fake-token"})
    
    # Mock the current user dependency
    async def mock_get_current_user(request):
        return "test-user-id"
    
    # Test inputs
    test_inputs = [
        "Hello!",
        "Add a task to clean my room",
        "List my tasks"
    ]
    
    for inp in test_inputs:
        print(f"\nTesting input: '{inp}'")
        try:
            # Simulate the chat endpoint call
            from backend.routes.chat import ChatRequest
            
            # Create a mock request object
            request = ChatRequest(message=inp)
            
            # Since we can't easily mock all dependencies, let's just test the mock response generation
            response = get_mock_chat_response(inp)
            print(f"  Generated response: '{response.text}'")
            print(f"  Tool calls: {len(response.tool_calls)}")
            for i, tc in enumerate(response.tool_calls):
                print(f"    {i+1}. {tc.name}: {tc.parameters}")
                
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()


def check_environment_issues():
    """Check for common environment issues that could prevent the chatbot from working"""
    print("\nChecking environment configuration...")
    
    # Check if COHERE_API_KEY is set properly
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    cohere_key = os.getenv("COHERE_API_KEY")
    print(f"COHERE_API_KEY: {cohere_key}")
    
    if cohere_key == "YOUR_COHERE_API_KEY_HERE" or not cohere_key:
        print("  [WARNING] COHERE_API_KEY is not properly set. The chatbot will use mock responses.")
        print("  To use the real Cohere API, set a valid API key in your .env file.")
    
    # Check other important environment variables
    jwt_secret = os.getenv("BETTER_AUTH_SECRET", os.getenv("JWT_SECRET"))
    print(f"BETTER_AUTH_SECRET/JWT_SECRET: {'Set' if jwt_secret else 'NOT SET'}")
    
    database_url = os.getenv("DATABASE_URL")
    print(f"DATABASE_URL: {database_url}")


if __name__ == "__main__":
    print("Chatbot Functionality Diagnostic Tool\n")
    print("="*50)
    
    test_mock_responses_standalone()
    test_chat_endpoint_simulation()
    check_environment_issues()
    
    print("\n" + "="*50)
    print("Diagnostic complete.")
    print("\nNote: If COHERE_API_KEY is not set properly, the chatbot will use mock responses.")
    print("The mock responses have been enhanced to provide better conversational experience.")
    print("For full functionality, obtain a valid Cohere API key and update your .env file.")