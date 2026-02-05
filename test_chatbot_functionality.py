"""
Test script to verify the chatbot's functionality for both task management and general conversation.
"""
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.mock_responses import get_mock_chat_response

def test_chatbot_functionality():
    print("Testing Chatbot Functionality...\n")
    
    test_cases = [
        # Greeting cases
        {"input": "Hello!", "type": "greeting"},
        {"input": "Hi there", "type": "greeting"},
        {"input": "Hey", "type": "greeting"},
        
        # General conversation
        {"input": "How are you?", "type": "general"},
        {"input": "What can you do?", "type": "general"},
        {"input": "Who are you?", "type": "general"},
        
        # Task management
        {"input": "Add a task to clean my room", "type": "task_management"},
        {"input": "Create a new task to buy groceries", "type": "task_management"},
        {"input": "Show me my tasks", "type": "task_management"},
        {"input": "List my tasks", "type": "task_management"},
        {"input": "I finished cleaning my room, mark it as done", "type": "task_management"},
        {"input": "Complete task 1", "type": "task_management"},
        {"input": "Delete the grocery task", "type": "task_management"},
        {"input": "Remove task 2", "type": "task_management"},
        {"input": "Edit task 1 to say 'clean bedroom'", "type": "task_management"},
        {"input": "Update the title of task 1", "type": "task_management"},
        
        # General conversation mixed with task requests
        {"input": "Can you help me organize my day? I need to add a few tasks.", "type": "mixed"},
        {"input": "What's up? Also, can you list my tasks?", "type": "mixed"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i:2d}. Input: \"{test_case['input']}\"")
        print(f"    Type: {test_case['type']}")
        
        response = get_mock_chat_response(test_case['input'])
        
        print(f"    Response: \"{response.text}\"")
        print(f"    Tool Calls: {len(response.tool_calls)}")
        for j, tool_call in enumerate(response.tool_calls, 1):
            print(f"      {j}. {tool_call.name}: {tool_call.parameters}")
        print()


def test_edge_cases():
    print("Testing Edge Cases...\n")
    
    edge_cases = [
        "Add a task",
        "List tasks",
        "Complete task",
        "Delete task",
        "Edit task",
        "Random message with no clear intent",
        "12345",  # Just numbers
        "",  # Empty string
        "   ",  # Whitespace only
    ]
    
    for i, test_case in enumerate(edge_cases, 1):
        print(f"{i:2d}. Input: \"{test_case}\"")
        
        response = get_mock_chat_response(test_case)
        
        print(f"    Response: \"{response.text}\"")
        print(f"    Tool Calls: {len(response.tool_calls)}")
        for j, tool_call in enumerate(response.tool_calls, 1):
            print(f"      {j}. {tool_call.name}: {tool_call.parameters}")
        print()


if __name__ == "__main__":
    test_chatbot_functionality()
    print("\n" + "="*60 + "\n")
    test_edge_cases()
    print("\nAll tests completed!")