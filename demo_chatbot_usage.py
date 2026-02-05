"""
Demonstration script showing how to properly use the chatbot with authentication.
This script registers a user, logs in, and then uses the chatbot.
"""
import requests
import json
import os
from datetime import datetime

def demo_chatbot_usage():
    """Demonstrate proper chatbot usage with authentication"""
    print("Chatbot Usage Demonstration")
    print("=" * 40)
    
    # Base URL for the API
    base_url = "http://localhost:8000/api"
    
    print("Step 1: Registering a test user...")
    register_data = {
        "email": "demo@example.com",
        "password": "demopassword123",
        "name": "Demo User"
    }
    
    try:
        register_response = requests.post(f"{base_url}/register", json=register_data)
        if register_response.status_code == 200:
            print("✓ User registered successfully")
            user_data = register_response.json()
        else:
            print(f"⚠ Registration response: {register_response.status_code} - {register_response.text}")
            # If user already exists, we'll proceed to login
    except Exception as e:
        print(f"⚠ Could not register user: {e}")
        print("Assuming user already exists, proceeding to login...")
    
    print("\nStep 2: Logging in to get authentication token...")
    login_data = {
        "email": "demo@example.com",
        "password": "demopassword123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/login", json=login_data)
        if login_response.status_code == 200:
            print("✓ Login successful")
            auth_data = login_response.json()
            token = auth_data["token"]
            print(f"  Token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {login_response.status_code} - {login_response.text}")
            return
    except Exception as e:
        print(f"✗ Login error: {e}")
        print("\nMake sure the backend server is running on http://localhost:8000")
        return
    
    print("\nStep 3: Setting up headers with authentication token...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("\nStep 4: Using the chatbot for various tasks...")
    
    # Test messages to send to the chatbot
    test_messages = [
        "Hello! How are you?",
        "Add a task to clean my room",
        "Add another task to buy groceries",
        "What can you do?",
        "List my tasks",
        "Complete task 1",
        "Edit task 2 to say 'buy groceries and milk'",
        "Delete task 2",
        "Goodbye!"
    ]
    
    conversation_id = None
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Sending: \"{message}\"")
        
        chat_data = {
            "message": message,
            "conversation_id": conversation_id
        }
        
        try:
            chat_response = requests.post(f"{base_url}/chat", json=chat_data, headers=headers)
            
            if chat_response.status_code == 200:
                response_data = chat_response.json()
                print(f"   Bot: {response_data['response']}")
                
                # Update conversation ID for ongoing conversation
                conversation_id = response_data['conversation_id']
                
                # Show any tool calls that were made
                if response_data.get('tool_calls'):
                    print(f"   🛠️  Tool calls: {len(response_data['tool_calls'])}")
                    for tool_call in response_data['tool_calls']:
                        print(f"      - {tool_call['name']}: {tool_call['arguments']}")
            else:
                print(f"   ✗ Error: {chat_response.status_code} - {chat_response.text}")
                
        except Exception as e:
            print(f"   ✗ Error sending message: {e}")
    
    print(f"\n{'='*40}")
    print("Demo completed!")
    print("\nNote: This demonstration works with both real Cohere API (if key is set)")
    print("and with enhanced mock responses (when no key is set).")
    print("\nTo get full AI capabilities, set your COHERE_API_KEY in the .env file.")


def check_backend_status():
    """Check if the backend is running"""
    print("Checking backend status...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Backend is running and healthy")
            return True
        else:
            print(f"✗ Backend responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Backend is not running. Please start it with: python run_backend.py")
        return False


if __name__ == "__main__":
    print("Chatbot Usage Demo")
    print("=" * 50)
    
    if check_backend_status():
        demo_chatbot_usage()
    else:
        print("\nPlease start the backend server before running this demo:")
        print("  python run_backend.py")