#!/usr/bin/env python3
"""Simple test script to check if the chat endpoint works"""

import sys
import os
sys.path.insert(0, '.')

from backend.main import app
from fastapi.testclient import TestClient

# Create a test client
client = TestClient(app)

# Test the chat endpoint
print("Testing chat endpoint...")
response = client.post(
    "/api/chat",
    json={"message": "Hello", "conversation_id": None},
    headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyLTkzNTMyIiwidXNlcl9pZCI6InVzZXItOTM1MzIiLCJlbWFpbCI6Im5ld3VzZXJAZXhhbXBsZS5jb20iLCJleHAiOjE3NzAyNDc1ODZ9.PdmAQDE-Rat7z_4Ymb8Vt6ww1CZYcz4K9VDWAoEcOmk"}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")