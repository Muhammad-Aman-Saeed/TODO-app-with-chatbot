#!/usr/bin/env python3
"""
Final verification script to ensure the backend authentication system is working properly.
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_auth_endpoints():
    print("Testing backend authentication endpoints...")
    
    # Test login endpoint
    print("\n1. Testing login endpoint:")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        headers={"Content-Type": "application/json"},
        json={"email": "test@example.com", "password": "password"}
    )
    print(f"   Status: {login_response.status_code}")
    if login_response.status_code == 200:
        print("   ✓ Login endpoint working correctly")
        response_data = login_response.json()
        print(f"   Token length: {len(response_data.get('token', ''))} characters")
    else:
        print(f"   ✗ Login endpoint failed: {login_response.text}")
        return False
    
    # Test register endpoint
    print("\n2. Testing register endpoint:")
    register_response = requests.post(
        f"{BASE_URL}/auth/register",
        headers={"Content-Type": "application/json"},
        json={"email": "newuser@example.com", "password": "password", "name": "New User"}
    )
    print(f"   Status: {register_response.status_code}")
    if register_response.status_code == 200:
        print("   ✓ Register endpoint working correctly")
        response_data = register_response.json()
        print(f"   Token length: {len(response_data.get('token', ''))} characters")
    else:
        print(f"   ✗ Register endpoint failed: {register_response.text}")
        return False
    
    # Test token validation with the login token
    print("\n3. Testing token validation:")
    token = login_response.json().get('token')
    if token:
        token_response = requests.get(
            f"{BASE_URL}/auth/token",
            headers={"Authorization": f"Bearer {token}"}
        )
        print(f"   Status: {token_response.status_code}")
        if token_response.status_code == 200:
            print("   ✓ Token validation working correctly")
        else:
            print(f"   ✗ Token validation failed: {token_response.text}")
            return False
    else:
        print("   ✗ No token to test with")
        return False
    
    print("\n✓ All authentication endpoints are working correctly!")
    return True

if __name__ == "__main__":
    print("Final verification of backend authentication system...")
    
    # Start the backend server
    import subprocess
    import time
    import os
    
    # Change to the project root directory
    os.chdir("..")
    
    # Start the backend server in a subprocess
    server_process = subprocess.Popen(["python", "run_backend.py"])
    
    # Wait for the server to start
    time.sleep(5)
    
    try:
        success = test_auth_endpoints()
        if success:
            print("\n🎉 Backend authentication system is fully functional!")
            print("\nThe 'Failed to fetch' error during sign-in should now be resolved.")
            print("Both login and register endpoints are working correctly.")
        else:
            print("\n❌ Backend authentication system has issues.")
    finally:
        # Terminate the server process
        server_process.terminate()
        server_process.wait()