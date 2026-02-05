"""
Cohere Tools Module

This module defines the tool schemas and execution functions for the AI chatbot.
Each tool follows Cohere's JSON schema format and includes proper validation
to ensure users can only operate on their own data.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import cohere
from sqlmodel import Session, select
from ..models import Task, Conversation, Message
from ..services.task_service import (
    add_task_service,
    list_tasks_service,
    complete_task_service,
    delete_task_service,
    edit_task_service,
    get_user_info_service
)


class AddTaskArgs(BaseModel):
    user_id: str
    title: str
    description: Optional[str] = None


class ListTasksArgs(BaseModel):
    user_id: str
    status: str = "all"


class CompleteTaskArgs(BaseModel):
    user_id: str
    task_id: int


class DeleteTaskArgs(BaseModel):
    user_id: str
    task_id: int


class EditTaskArgs(BaseModel):
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class GetUserInfoArgs(BaseModel):
    user_id: str


def validate_user_access(requested_user_id: str, authenticated_user_id: str) -> bool:
    """
    Validate that the requested user ID matches the authenticated user ID
    """
    return requested_user_id == authenticated_user_id


def execute_add_task(args: AddTaskArgs, authenticated_user_id: str) -> Dict[str, Any]:
    """
    Execute the add_task tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot add task for another user")
    
    result = add_task_service(
        user_id=args.user_id,
        title=args.title,
        description=args.description
    )
    return result


def execute_list_tasks(args: ListTasksArgs, authenticated_user_id: str) -> List[Dict[str, Any]]:
    """
    Execute the list_tasks tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot list tasks for another user")
    
    result = list_tasks_service(
        user_id=args.user_id,
        status=args.status
    )
    return result


def execute_complete_task(args: CompleteTaskArgs, authenticated_user_id: str) -> Dict[str, Any]:
    """
    Execute the complete_task tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot complete task for another user")
    
    result = complete_task_service(
        user_id=args.user_id,
        task_id=args.task_id
    )
    return result


def execute_delete_task(args: DeleteTaskArgs, authenticated_user_id: str) -> Dict[str, Any]:
    """
    Execute the delete_task tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot delete task for another user")

    result = delete_task_service(
        user_id=args.user_id,
        task_id=args.task_id
    )
    return result


def execute_edit_task(args: EditTaskArgs, authenticated_user_id: str) -> Dict[str, Any]:
    """
    Execute the edit_task tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot edit task for another user")

    result = edit_task_service(
        user_id=args.user_id,
        task_id=args.task_id,
        title=args.title,
        description=args.description,
        completed=args.completed
    )
    return result


def execute_get_user_info(args: GetUserInfoArgs, authenticated_user_id: str) -> Dict[str, Any]:
    """
    Execute the get_user_info tool
    """
    if not validate_user_access(args.user_id, authenticated_user_id):
        raise ValueError("Unauthorized: Cannot access another user's information")
    
    result = get_user_info_service(
        user_id=args.user_id
    )
    return result


# Define the Cohere tool schemas
COHERE_TOOLS = [
    {
        "name": "add_task",
        "description": "Add a new task for the user",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user who owns the task",
                "type": "str",
                "required": True
            },
            "title": {
                "description": "The title of the task",
                "type": "str",
                "required": True
            },
            "description": {
                "description": "An optional description of the task",
                "type": "str",
                "required": False
            }
        }
    },
    {
        "name": "list_tasks",
        "description": "List tasks for the user",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user whose tasks to list",
                "type": "str",
                "required": True
            },
            "status": {
                "description": "Filter tasks by status ('all', 'pending', 'completed')",
                "type": "str",
                "required": False,
                "default": "all"
            }
        }
    },
    {
        "name": "complete_task",
        "description": "Mark a task as completed",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user who owns the task",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to complete",
                "type": "int",
                "required": True
            }
        }
    },
    {
        "name": "delete_task",
        "description": "Delete a task",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user who owns the task",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to delete",
                "type": "int",
                "required": True
            }
        }
    },
    {
        "name": "edit_task",
        "description": "Edit an existing task (title, description, or completion status)",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user who owns the task",
                "type": "str",
                "required": True
            },
            "task_id": {
                "description": "The ID of the task to edit",
                "type": "int",
                "required": True
            },
            "title": {
                "description": "The new title for the task (optional)",
                "type": "str",
                "required": False
            },
            "description": {
                "description": "The new description for the task (optional)",
                "type": "str",
                "required": False
            },
            "completed": {
                "description": "Whether the task is completed (optional)",
                "type": "bool",
                "required": False
            }
        }
    },
    {
        "name": "get_user_info",
        "description": "Get user's profile information",
        "parameter_definitions": {
            "user_id": {
                "description": "The ID of the user whose information to retrieve",
                "type": "str",
                "required": True
            }
        }
    }
]