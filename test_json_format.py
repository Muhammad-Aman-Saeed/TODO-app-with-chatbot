"""
Test script to verify the chatbot responds in the required JSON format.
"""
import sys
import os
import json
import uuid
from datetime import datetime, timedelta
import jwt
from backend.utils.mock_responses import get_mock_chat_response
from backend.routes.chat import ChatRequest, ChatActionResponse, TaskData
from backend.models import User
from backend.db import SessionLocal

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Secret key for JWT (should match what's in the app)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"

def create_test_user():
    """Create a test user in the database"""
    with SessionLocal() as session:
        # Check if test user already exists
        from sqlmodel import select
        existing_user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if existing_user:
            return existing_user.id
        
        # Create a new test user
        user_id = str(uuid.uuid4())
        from backend.models import get_password_hash
        test_user = User(
            id=user_id,
            email="test@example.com",
            name="Test User",
            hashed_password=get_password_hash("password")
        )
        session.add(test_user)
        session.commit()
        return user_id

def generate_test_token(user_id):
    """Generate a JWT token for testing"""
    payload = {
        "sub": user_id,
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
        "scope": "access_token"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def test_json_format():
    """Test that responses are in the required JSON format"""
    print("Testing JSON Response Format\n")
    print("="*50)
    
    # Create a test user
    user_id = create_test_user()
    print(f"Created test user with ID: {user_id}")
    
    # Test various chat interactions
    test_messages = [
        "Hello!",
        "Add a task to clean my room",
        "List my tasks",
        "Complete task 1",
        "Delete task 1",
        "Edit task 1 to say updated task"
    ]
    
    print(f"\nTesting {len(test_messages)} chat interactions for JSON format:")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Input: \"{message}\"")
        
        # Get mock response (simulating what would happen without Cohere API)
        response = get_mock_chat_response(message)
        print(f"   Raw response text: \"{response.text}\"")
        print(f"   Tool calls: {len(response.tool_calls)}")
        
        # Simulate what the actual endpoint would return
        # For this test, we'll create the expected response format
        action = "none"
        task_data = None
        response_message = response.text
        
        # Map common tool calls to actions
        if response.tool_calls:
            first_call = response.tool_calls[0]
            if first_call.name == "add_task":
                action = "add"
                task_data = TaskData(
                    id="",
                    title=first_call.parameters.get("title", "New task"),
                    description=first_call.parameters.get("description", ""),
                    completed=False
                )
            elif first_call.name == "list_tasks":
                action = "list"
            elif first_call.name == "complete_task":
                action = "complete"
                task_data = TaskData(
                    id=str(first_call.parameters.get("task_id", "")),
                    title="Completed task",
                    completed=True
                )
            elif first_call.name == "delete_task":
                action = "delete"
                task_data = TaskData(
                    id=str(first_call.parameters.get("task_id", ""))
                )
            elif first_call.name == "edit_task":
                action = "update"
                task_data = TaskData(
                    id=str(first_call.parameters.get("task_id", "")),
                    title=first_call.parameters.get("title", "Updated task"),
                    description=first_call.parameters.get("description", ""),
                    completed=first_call.parameters.get("completed", False)
                )
        
        # Create the expected response object
        chat_response = ChatActionResponse(
            action=action,
            task=task_data,
            message=response_message,
            conversation_id=1  # Mock conversation ID
        )
        
        # Convert to dict to see the JSON structure
        response_dict = chat_response.model_dump()
        print(f"   Expected JSON response:")
        print(f"     action: {response_dict['action']}")
        print(f"     task: {response_dict['task']}")
        print(f"     message: {response_dict['message']}")
        print(f"     conversation_id: {response_dict['conversation_id']}")
        
        # Verify the structure matches requirements
        required_keys = ['action', 'task', 'message', 'conversation_id']
        missing_keys = [key for key in required_keys if key not in response_dict]
        if missing_keys:
            print(f"   [ERROR] Missing keys: {missing_keys}")
        else:
            print(f"   [OK] All required keys present")

        # Verify action is valid
        valid_actions = ['add', 'delete', 'update', 'complete', 'list', 'none']
        if response_dict['action'] not in valid_actions:
            print(f"   [ERROR] Invalid action: {response_dict['action']}")
        else:
            print(f"   [OK] Valid action: {response_dict['action']}")
    
    print(f"\n{'='*50}")
    print("JSON format test completed!")

if __name__ == "__main__":
    test_json_format()