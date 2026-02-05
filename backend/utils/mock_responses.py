"""
Mock Responses Module

This module provides mock responses for when the Cohere API is not available,
allowing the application to run in development mode without requiring an API key.
"""

import random
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class MockToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]


class MockCohereResponse:
    def __init__(self, text: str = "", tool_calls: Optional[List[MockToolCall]] = None):
        self.text = text
        self.tool_calls = tool_calls or []


def get_mock_chat_response(message: str) -> MockCohereResponse:
    """
    Generate a mock response based on the input message.

    Args:
        message: The user's input message

    Returns:
        A mock Cohere response object
    """
    # Convert message to lowercase for easier matching
    message_lower = message.lower().strip()

    # Check for greetings first
    greeting_keywords = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    if any(greeting in message_lower for greeting in greeting_keywords):
        greetings = [
            "Hello! I'm your AI assistant. How can I help you today?",
            "Hi there! I'm here to assist you with managing your tasks. What would you like to do?",
            "Greetings! I'm your personal task assistant. Feel free to ask me to add, list, complete, or delete tasks."
        ]
        response_text = random.choice(greetings)
        return MockCohereResponse(text=response_text, tool_calls=[])

    # Check for general conversation
    general_keywords = ["how are you", "what can you do", "help", "what's up", "what are you", "who are you"]
    if any(keyword in message_lower for keyword in general_keywords):
        responses = [
            "I'm an AI assistant designed to help you manage your tasks. You can ask me to add, list, complete, edit, or delete tasks. How can I assist you today?",
            "I'm here to help you stay organized! I can manage your to-do list, track your progress, and keep you on schedule. What would you like to do?",
            "I'm your personal task manager AI. I can help you create tasks, mark them as complete, update them, or remove them. Just tell me what you need!"
        ]
        response_text = random.choice(responses)
        return MockCohereResponse(text=response_text, tool_calls=[])

    # Check for user info requests
    user_info_keywords = ["who am i", "user info", "profile", "about me", "my info"]
    if any(keyword in message_lower for keyword in user_info_keywords):
        return MockCohereResponse(
            text="I found your account information. You're a valued user of our task management system.",
            tool_calls=[
                MockToolCall(
                    name="get_user_info",
                    parameters={
                        "user_id": "mock-user-id"
                    }
                )
            ]
        )

    # Check for task listing
    list_indicators = ["list", "show", "view", "my tasks", "see", "display"]
    if any(indicator in message_lower for indicator in list_indicators):
        return MockCohereResponse(
            text="Here are your tasks with their IDs for easy reference. You can use the ID numbers to edit, complete, or delete specific tasks.",
            tool_calls=[
                MockToolCall(
                    name="list_tasks",
                    parameters={
                        "user_id": "mock-user-id",
                        "status": "all"
                    }
                )
            ]
        )

    # Check for task completion
    complete_indicators = ["complete", "done", "finish", "finished", "mark as done"]
    if any(indicator in message_lower for indicator in complete_indicators):
        # Try to extract task ID or title from the message
        task_identifier = "the task"
        task_id = 1

        # Look for numbers in the message (potential task IDs)
        words = message_lower.split()
        for word in words:
            if word.isdigit():
                task_identifier = f"task #{word}"
                task_id = int(word)
                break

        return MockCohereResponse(
            text=f"I've marked {task_identifier} as completed. Great job on finishing that!",
            tool_calls=[
                MockToolCall(
                    name="complete_task",
                    parameters={
                        "user_id": "mock-user-id",
                        "task_id": task_id
                    }
                )
            ]
        )

    # Check for task deletion
    delete_indicators = ["delete", "remove", "cancel", "get rid of", "eliminate"]
    if any(indicator in message_lower for indicator in delete_indicators):
        # Try to extract task ID or title from the message
        task_identifier = "the task"
        task_id = 1

        # Look for numbers in the message (potential task IDs)
        words = message_lower.split()
        for word in words:
            if word.isdigit():
                task_identifier = f"task #{word}"
                task_id = int(word)
                break

        return MockCohereResponse(
            text=f"I've removed {task_identifier} from your task list.",
            tool_calls=[
                MockToolCall(
                    name="delete_task",
                    parameters={
                        "user_id": "mock-user-id",
                        "task_id": task_id
                    }
                )
            ]
        )

    # Check for task editing
    edit_indicators = ["edit", "update", "change", "modify", "adjust", "fix"]
    if any(indicator in message_lower for indicator in edit_indicators):
        # Try to extract task ID and what to edit
        task_id = 1
        title = None
        description = None

        # Look for numbers (potential task IDs)
        words = message_lower.split()
        for word in words:
            if word.isdigit():
                task_id = int(word)
                break

        # For simplicity, assume the user wants to update the title with the rest of the message
        # In a real implementation, we'd parse more specifically
        if "to" in message:
            # Extract text after "to"
            parts = message.split("to", 1)
            if len(parts) > 1:
                title = parts[1].strip()
            else:
                title = message.split("edit", 1)[1].strip() if "edit" in message else "Updated task"
        else:
            title = message.split("edit", 1)[1].strip() if "edit" in message else "Updated task"

        return MockCohereResponse(
            text=f"I've updated your task. How does this look?",
            tool_calls=[
                MockToolCall(
                    name="edit_task",
                    parameters={
                        "user_id": "mock-user-id",
                        "task_id": task_id,
                        "title": title
                    }
                )
            ]
        )

    # Check for task creation
    task_indicators = ["task", "add", "create", "new", "todo", "to-do", "to do"]
    if any(indicator in message_lower for indicator in task_indicators):
        # Extract potential task title from the message
        # Find the part after task-related keywords
        task_title = "New task"

        # Find the first task indicator and extract text after it
        for indicator in task_indicators:
            if indicator in message_lower:
                # Get the part after the indicator
                idx = message_lower.find(indicator) + len(indicator)
                remaining = message_lower[idx:].strip()
                if remaining:
                    # Take the first few words as the task title
                    words = remaining.split()[:5]  # Take up to 5 words
                    task_title = " ".join(words).strip().capitalize()
                    # Remove punctuation at the end
                    task_title = task_title.rstrip('.,!?')
                    break

        # If we still have a generic title, try to get more meaningful text
        if task_title == "New task" or task_title == "Task" or task_title == "":
            # Use the whole message minus the indicators
            for indicator in task_indicators:
                message_lower = message_lower.replace(indicator, "").strip()
            words = message_lower.split()[:5]
            if words:
                task_title = " ".join(words).strip().capitalize()

        if task_title == "" or task_title.strip() == "":
            task_title = "New task"

        return MockCohereResponse(
            text=f"I've added '{task_title}' to your task list. Is there anything else you'd like to do?",
            tool_calls=[
                MockToolCall(
                    name="add_task",
                    parameters={
                        "user_id": "mock-user-id",
                        "title": task_title,
                        "description": f"Created based on your request: {message}"
                    }
                )
            ]
        )

    # Default response for general conversation
    else:
        # Generate more natural, conversational responses
        general_responses = [
            f"I understand you're saying: '{message}'. I'm here to help you manage your tasks. You can ask me to add, list, complete, edit, or delete tasks.",
            f"Thanks for your message: '{message}'. How can I assist you with your tasks today?",
            f"I received your message: '{message}'. I specialize in helping you organize your tasks. Would you like me to help you with something specific?",
            f"Noted: '{message}'. I'm your AI assistant for task management. I can help you create, update, complete, or remove tasks. What would you like to do?",
            f"Got it: '{message}'. I'm here to make managing your tasks easier. Is there something specific you'd like help with?"
        ]

        response_text = random.choice(general_responses)
        return MockCohereResponse(text=response_text, tool_calls=[])