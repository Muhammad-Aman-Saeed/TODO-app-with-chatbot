"""
Comprehensive test to verify the chatbot functionality with the required JSON format.
"""
import subprocess
import time
import requests
import json
import threading
import sys
import os

def start_server():
    """Start the backend server in a separate thread"""
    print("Starting backend server...")
    try:
        # Start the server in a subprocess
        proc = subprocess.Popen([
            sys.executable, "-c", 
            "from backend.main import app; import uvicorn; uvicorn.run(app, host='127.0.0.1', port=8000)"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Give the server some time to start
        time.sleep(5)
        
        # Check if the process is still running
        if proc.poll() is not None:
            # Server failed to start, get the error
            _, stderr = proc.communicate()
            print(f"Server failed to start. Error: {stderr.decode()}")
            return None
        
        print("Backend server started successfully!")
        return proc
        
    except Exception as e:
        print(f"Error starting backend: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_health():
    """Test if the server is running"""
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        return response.status_code == 200
    except:
        return False


def register_and_login():
    """Register a test user and get an authentication token"""
    # Register user
    register_data = {
        "email": "chatbot-test@example.com",
        "password": "securepassword123",
        "name": "Chatbot Test User"
    }
    
    try:
        register_response = requests.post("http://127.0.0.1:8000/api/register", json=register_data)
        if register_response.status_code not in [200, 400]:  # 400 might mean user already exists
            print(f"Registration failed: {register_response.status_code} - {register_response.text}")
            return None
            
        # Login to get token
        login_data = {
            "email": "chatbot-test@example.com",
            "password": "securepassword123"
        }
        
        login_response = requests.post("http://127.0.0.1:8000/api/login", json=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code} - {login_response.text}")
            return None
            
        token = login_response.json()["token"]
        print("Authentication successful!")
        return token
        
    except Exception as e:
        print(f"Authentication error: {e}")
        return None


def test_chat_json_format(token):
    """Test the chat endpoint to ensure it returns the correct JSON format"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_cases = [
        {
            "input": "Hello!",
            "expected_action": "none",
            "description": "Greeting message"
        },
        {
            "input": "Add a task to clean my room",
            "expected_action": "add",
            "description": "Add task command"
        },
        {
            "input": "List my tasks",
            "expected_action": "list",
            "description": "List tasks command"
        },
        {
            "input": "Complete task 1",
            "expected_action": "complete",
            "description": "Complete task command"
        },
        {
            "input": "Delete task 1",
            "expected_action": "delete",
            "description": "Delete task command"
        }
    ]
    
    print(f"\nTesting {len(test_cases)} chat interactions for JSON format...")
    
    all_passed = True
    conversation_id = None
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: \"{test_case['input']}\"")
        
        chat_data = {
            "message": test_case["input"],
            "conversation_id": conversation_id
        }
        
        try:
            response = requests.post("http://127.0.0.1:8000/api/chat", json=chat_data, headers=headers)
            
            if response.status_code != 200:
                print(f"   [ERROR] Request failed: {response.status_code} - {response.text}")
                all_passed = False
                continue

            # Parse the response
            response_data = response.json()

            # Check required fields
            required_fields = ["action", "task", "message", "conversation_id"]
            missing_fields = [field for field in required_fields if field not in response_data]

            if missing_fields:
                print(f"   [ERROR] Missing fields: {missing_fields}")
                all_passed = False
                continue

            # Check action value
            action = response_data["action"]
            valid_actions = ["add", "delete", "update", "complete", "list", "none"]

            if action not in valid_actions:
                print(f"   [ERROR] Invalid action: {action}")
                all_passed = False
                continue

            # Check if action matches expectation
            expected_action = test_case["expected_action"]
            if action != expected_action:
                print(f"   [WARN] Action mismatch: expected '{expected_action}', got '{action}'")
                # Don't fail the test for this, as AI behavior can vary

            # Check task field structure (if not null)
            task = response_data["task"]
            if task is not None:
                task_required_fields = ["id", "title", "description", "completed"]
                if isinstance(task, dict):
                    missing_task_fields = [field for field in task_required_fields if field not in task]
                    if missing_task_fields:
                        print(f"   [ERROR] Missing task fields: {missing_task_fields}")
                        all_passed = False
                        continue
                else:
                    print(f"   [ERROR] Task field is not a dictionary: {type(task)}")
                    all_passed = False
                    continue

            # Update conversation_id for next request
            conversation_id = response_data["conversation_id"]

            print(f"   [OK] Action: {action}")
            print(f"   [OK] Task: {task is not None}")
            print(f"   [OK] Message: \"{response_data['message'][:50]}...\"")
            print(f"   [OK] Conversation ID: {conversation_id}")

        except json.JSONDecodeError:
            print(f"   [ERROR] Response is not valid JSON: {response.text[:100]}")
            all_passed = False
        except Exception as e:
            print(f"   [ERROR] Error: {e}")
            all_passed = False
    
    return all_passed


def main():
    print("Comprehensive Chatbot JSON Format Test")
    print("=" * 50)
    
    # Start the server
    server_proc = start_server()
    if not server_proc:
        print("[ERROR] Failed to start server")
        return False

    # Wait a bit more for server to be ready
    time.sleep(2)

    # Test if server is running
    if not test_health():
        print("[ERROR] Server health check failed")
        server_proc.terminate()
        return False

    print("[OK] Server is running and healthy")

    # Register user and get token
    token = register_and_login()
    if not token:
        print("[ERROR] Authentication failed")
        server_proc.terminate()
        return False
    
    # Test chat functionality
    success = test_chat_json_format(token)
    
    # Terminate the server
    server_proc.terminate()
    server_proc.wait()
    
    print(f"\n{'='*50}")
    if success:
        print("[SUCCESS] All tests passed! Chatbot is responding in the correct JSON format.")
    else:
        print("[ERROR] Some tests failed. Please check the implementation.")

    return success


if __name__ == "__main__":
    main()