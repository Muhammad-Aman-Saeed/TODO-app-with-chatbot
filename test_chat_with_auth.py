"""
Test script to verify the chatbot functionality with simulated authentication.
"""
import sys
import os
import uuid
from datetime import datetime, timedelta
import jwt
from backend.utils.mock_responses import get_mock_chat_response
from backend.routes.chat import ChatRequest
from backend.models import User
from backend.db import SessionLocal
from backend.services.task_service import add_task_service, list_tasks_service

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Secret key for JWT (should match what's in the app)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "zF4Gr5uYTUtVZVcyXGLFaTyskJhewCl5")
ALGORITHM = "HS256"

def create_test_user():
    """Create a test user in the database"""
    with SessionLocal() as session:
        # Check if test user already exists
        existing_user = session.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            return existing_user.id
        
        # Create a new test user
        user_id = str(uuid.uuid4())
        test_user = User(
            id=user_id,
            email="test@example.com",
            name="Test User",
            hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"  # bcrypt hash for "password"
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

def test_chat_functionality():
    """Test the chat functionality with proper authentication"""
    print("Testing Chat Functionality with Authentication\n")
    print("="*50)
    
    # Create a test user
    user_id = create_test_user()
    print(f"Created test user with ID: {user_id}")
    
    # Generate a test token
    token = generate_test_token(user_id)
    print(f"Generated test token: {token[:20]}...")
    
    # Test various chat interactions
    test_messages = [
        "Hello!",
        "Add a task to clean my room",
        "Add another task to buy groceries",
        "List my tasks",
        "Complete task 1",
        "Edit task 2 to say 'buy groceries and milk'",
        "Delete task 2",
        "What can you do?",
        "How are you?"
    ]
    
    print(f"\nTesting {len(test_messages)} chat interactions:")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: \"{message}\"")
        
        # Get mock response (simulating what would happen without Cohere API)
        response = get_mock_chat_response(message)
        print(f"   Bot: \"{response.text}\"")
        
        if response.tool_calls:
            print(f"   Tool calls: {len(response.tool_calls)}")
            for j, tool_call in enumerate(response.tool_calls, 1):
                print(f"     {j}. {tool_call.name}: {tool_call.parameters}")
                
                # Simulate executing the tool with the test user
                try:
                    if tool_call.name == "add_task":
                        result = add_task_service(
                            user_id=user_id,
                            title=tool_call.parameters.get("title", "Test task"),
                            description=tool_call.parameters.get("description")
                        )
                        print(f"         -> Executed: {result}")
                        
                    elif tool_call.name == "list_tasks":
                        status = tool_call.parameters.get("status", "all")
                        result = list_tasks_service(user_id=user_id, status=status)
                        print(f"         -> Found {len(result)} tasks")
                        
                except Exception as e:
                    print(f"         -> Error executing tool: {e}")
    
    print(f"\n{'='*50}")
    print("Chat functionality test completed!")
    print("\nNote: This test simulates the chat functionality using mock responses.")
    print("In a real scenario with Cohere API key, the responses would come from the AI model.")

if __name__ == "__main__":
    test_chat_functionality()