#!/usr/bin/env python3
"""Simple test to verify the chat functionality works"""

import sys
import os
sys.path.insert(0, '.')

# Test that the modules can be imported properly
try:
    from backend.main import app
    print("[OK] Successfully imported backend app")
except Exception as e:
    print(f"[ERROR] Failed to import backend app: {e}")
    sys.exit(1)

# Test the chat endpoint using TestClient
try:
    from fastapi.testclient import TestClient
    client = TestClient(app)

    # Test the chat endpoint
    response = client.post(
        "/api/chat",
        json={"message": "Hello", "conversation_id": None},
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTkzNTMyIiwidXNlcl9pZCI6InVzZXItOTM1MzIiLCJlbWFpbCI6Im5ld3VzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE3NzAyNDc1ODZ9.PdmAQDE-Rat7z_4Ymb8Vt6ww1CZYcz4K9VDWAoEcOmk"}
    )

    print(f"[OK] Chat endpoint test completed with status code: {response.status_code}")
    if response.status_code == 200:
        print("[OK] Chat endpoint is working correctly!")
        print(f"Response: {response.json()}")
    else:
        print(f"[ERROR] Chat endpoint returned error: {response.text}")

except Exception as e:
    print(f"[ERROR] Error testing chat endpoint: {e}")
    import traceback
    traceback.print_exc()