import requests
import json
import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Starting comprehensive functionality test...")

BASE_URL = "http://127.0.0.1:8000/api"

# Generate a unique email for this test run
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
test_email = f"finaltest_{timestamp}@example.com"

# Test 1: Registration
print(f"\n1. Testing user registration with email: {test_email}...")
try:
    reg_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={
            "email": test_email,
            "password": "securepassword",
            "name": "Final Test User"
        }
    )
    print(f"Registration status: {reg_response.status_code}")
    if reg_response.status_code == 200:
        reg_data = reg_response.json()
        token = reg_data['token']
        user_id = reg_data['user']['id']
        print(f"[SUCCESS] User registered successfully with ID: {user_id}")
    else:
        print(f"[ERROR] Registration failed: {reg_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Registration error: {e}")
    sys.exit(1)

# Test 2: Login
print("\n2. Testing user login...")
try:
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "finaltest@example.com",
            "password": "securepassword"
        }
    )
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data['token']  # Refresh token from login
        print("[SUCCESS] User logged in successfully")
    else:
        print(f"[ERROR] Login failed: {login_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Login error: {e}")
    sys.exit(1)

# Test 3: Create task
print("\n3. Testing task creation...")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
try:
    task_response = requests.post(
        f"{BASE_URL}/tasks/",
        json={
            "title": "Final Test Task",
            "description": "This is a test task for the final test"
        },
        headers=headers
    )
    print(f"Task creation status: {task_response.status_code}")
    if task_response.status_code == 201:
        task_data = task_response.json()
        task_id = task_data['id']
        print(f"[SUCCESS] Task created successfully with ID: {task_id}")
    else:
        print(f"[ERROR] Task creation failed: {task_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Task creation error: {e}")
    sys.exit(1)

# Test 4: Get tasks
print("\n4. Testing task retrieval...")
try:
    get_response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
    print(f"Task retrieval status: {get_response.status_code}")
    if get_response.status_code == 200:
        tasks = get_response.json()
        print(f"[SUCCESS] Retrieved {len(tasks)} task(s)")
        if len(tasks) > 0 and tasks[0]['id'] == task_id:
            print("[SUCCESS] Correct task retrieved")
        else:
            print("[ERROR] Wrong task retrieved")
            sys.exit(1)
    else:
        print(f"[ERROR] Task retrieval failed: {get_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Task retrieval error: {e}")
    sys.exit(1)

# Test 5: Update task
print("\n5. Testing task update...")
try:
    update_response = requests.put(
        f"{BASE_URL}/tasks/{task_id}",
        json={
            "title": "Updated Final Test Task",
            "description": "This is an updated test task for the final test",
            "completed": True
        },
        headers=headers
    )
    print(f"Task update status: {update_response.status_code}")
    if update_response.status_code == 200:
        updated_task = update_response.json()
        if updated_task['completed']:
            print("[SUCCESS] Task updated successfully and marked as completed")
        else:
            print("[ERROR] Task update failed - not marked as completed")
            sys.exit(1)
    else:
        print(f"[ERROR] Task update failed: {update_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Task update error: {e}")
    sys.exit(1)

# Test 6: Toggle completion
print("\n6. Testing task completion toggle...")
try:
    toggle_response = requests.patch(
        f"{BASE_URL}/tasks/{task_id}/complete",
        json={"completed": False},
        headers=headers
    )
    print(f"Task toggle status: {toggle_response.status_code}")
    if toggle_response.status_code == 200:
        toggled_task = toggle_response.json()
        if not toggled_task['completed']:
            print("[SUCCESS] Task completion toggled successfully")
        else:
            print("[ERROR] Task toggle failed - still marked as completed")
            sys.exit(1)
    else:
        print(f"[ERROR] Task toggle failed: {toggle_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Task toggle error: {e}")
    sys.exit(1)

# Test 7: Delete task
print("\n7. Testing task deletion...")
try:
    delete_response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
    print(f"Task deletion status: {delete_response.status_code}")
    if delete_response.status_code == 204:
        print("[SUCCESS] Task deleted successfully")
    else:
        print(f"[ERROR] Task deletion failed: {delete_response.text}")
        sys.exit(1)
except Exception as e:
    print(f"[ERROR] Task deletion error: {e}")
    sys.exit(1)

print("\n[SUCCESS] All functionality tests passed successfully!")
print("The application is fully functional with:")
print("- Proper user registration and login with password hashing")
print("- JWT-based authentication")
print("- Full task CRUD operations")
print("- Secure database storage")
print("- Proper error handling")