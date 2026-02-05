"""
Test script to verify the backend chat API is working properly
"""
import requests
import json

def test_backend_chat():
    print("Testing Backend Chat API...")
    
    # Test URL - adjust as needed
    url = "http://localhost:8000/api/chat"
    
    # Test with a dummy token (will fail authentication, but shows if endpoint exists)
    headers = {
        "Authorization": "Bearer dummy-token",
        "Content-Type": "application/json"
    }
    
    # Test message
    data = {
        "message": "Hello",
        "conversation_id": None
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 401:
            print("✓ Endpoint exists (401 Unauthorized - expected without valid token)")
        elif response.status_code == 200:
            print("✓ Endpoint working (200 OK)")
            print(f"Response: {response.json()}")
        else:
            print(f"Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        print("Make sure the backend server is running on http://localhost:8000")

def test_expected_format():
    print("\nExpected response format:")
    print(json.dumps({
        "action": "none",
        "task": None,
        "message": "Hello! How can I help with your tasks?",
        "conversation_id": 1
    }, indent=2))

if __name__ == "__main__":
    test_backend_chat()
    test_expected_format()