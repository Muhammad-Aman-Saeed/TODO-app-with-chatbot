"""
Sample chat interactions demonstrating the chatbot's task management capabilities.
This shows how users can interact with the chatbot to add, complete, delete, and edit tasks.
"""
import json

sample_interactions = {
    "add_task": {
        "user_input": "I need to add a task to clean my room",
        "expected_tool_call": {
            "name": "add_task",
            "arguments": {
                "user_id": "current_user_id",
                "title": "Clean my room",
                "description": None
            }
        },
        "chatbot_response": "I've added the task 'Clean my room' to your to-do list. Is there anything else you'd like to do?"
    },
    "add_task_with_description": {
        "user_input": "Add a task to buy groceries, and the description is 'milk, bread, eggs, and fruits'",
        "expected_tool_call": {
            "name": "add_task",
            "arguments": {
                "user_id": "current_user_id",
                "title": "Buy groceries",
                "description": "milk, bread, eggs, and fruits"
            }
        },
        "chatbot_response": "I've added the task 'Buy groceries' with the description 'milk, bread, eggs, and fruits' to your to-do list."
    },
    "list_tasks": {
        "user_input": "What tasks do I have?",
        "expected_tool_call": {
            "name": "list_tasks",
            "arguments": {
                "user_id": "current_user_id",
                "status": "all"
            }
        },
        "chatbot_response": "You have the following tasks:\n1. Clean my room (Pending)\n2. Buy groceries (Pending)"
    },
    "complete_task": {
        "user_input": "I finished cleaning my room, mark it as completed",
        "expected_tool_call": {
            "name": "complete_task",
            "arguments": {
                "user_id": "current_user_id",
                "task_id": 1
            }
        },
        "chatbot_response": "Great job! I've marked 'Clean my room' as completed. You're making excellent progress!"
    },
    "edit_task": {
        "user_input": "Change the description of my grocery task to 'milk, bread, eggs, fruits, and vegetables'",
        "expected_tool_call": {
            "name": "edit_task",
            "arguments": {
                "user_id": "current_user_id",
                "task_id": 2,
                "description": "milk, bread, eggs, fruits, and vegetables"
            }
        },
        "chatbot_response": "I've updated the description for 'Buy groceries' to 'milk, bread, eggs, fruits, and vegetables'."
    },
    "edit_task_title": {
        "user_input": "Change the title of task 2 to 'Go grocery shopping'",
        "expected_tool_call": {
            "name": "edit_task",
            "arguments": {
                "user_id": "current_user_id",
                "task_id": 2,
                "title": "Go grocery shopping"
            }
        },
        "chatbot_response": "I've updated the title of your task from 'Buy groceries' to 'Go grocery shopping'."
    },
    "delete_task": {
        "user_input": "I don't need to go grocery shopping anymore, delete that task",
        "expected_tool_call": {
            "name": "delete_task",
            "arguments": {
                "user_id": "current_user_id",
                "task_id": 2
            }
        },
        "chatbot_response": "I've removed the task 'Go grocery shopping' from your to-do list."
    },
    "complex_interaction": {
        "user_input": "I want to add a task to finish my project by Friday, then mark my room cleaning task as done",
        "expected_tool_calls": [
            {
                "name": "add_task",
                "arguments": {
                    "user_id": "current_user_id",
                    "title": "Finish my project",
                    "description": "Complete the project by Friday"
                }
            },
            {
                "name": "complete_task",
                "arguments": {
                    "user_id": "current_user_id",
                    "task_id": 1
                }
            }
        ],
        "chatbot_response": "I've added the task 'Finish my project' with the description 'Complete the project by Friday' and marked 'Clean my room' as completed. You're doing great!"
    }
}

def display_sample_interactions():
    print("Sample Chat Interactions with Task Management Capabilities\n")
    print("="*60)
    
    for interaction_type, interaction_data in sample_interactions.items():
        print(f"\nInteraction Type: {interaction_type.replace('_', ' ').title()}")
        print("-" * 40)
        print(f"User: \"{interaction_data['user_input']}\"")
        
        if 'expected_tool_calls' in interaction_data:  # Multiple tool calls
            print("Expected Tool Calls:")
            for i, tool_call in enumerate(interaction_data['expected_tool_calls']):
                print(f"  {i+1}. {tool_call['name']}: {json.dumps(tool_call['arguments'])}")
        else:  # Single tool call
            print(f"Expected Tool Call: {interaction_data['expected_tool_call']['name']}: "
                  f"{json.dumps(interaction_data['expected_tool_call']['arguments'])}")
        
        print(f"Chatbot: \"{interaction_data['chatbot_response']}\"")
        print()

if __name__ == "__main__":
    display_sample_interactions()