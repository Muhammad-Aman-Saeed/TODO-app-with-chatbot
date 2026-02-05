"""
Task Service Module

This module implements the service functions that execute the tools with proper user validation.
It reuses existing Phase II CRUD operations with user_id validation.
"""

from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from ..models import Task
from ..dependencies import get_current_user
import logging

logger = logging.getLogger(__name__)


def add_task_service(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Service function to add a new task
    """
    from ..db import SessionLocal

    with SessionLocal() as session:
        # Create new task
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        logger.info(f"Task added: {task.id} for user: {user_id}")
        
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }


def list_tasks_service(user_id: str, status: str = "all") -> List[Dict[str, Any]]:
    """
    Service function to list tasks for a user
    """
    from ..db import SessionLocal

    with SessionLocal() as session:
        # Build query based on status filter
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        tasks = session.exec(query).all()

        logger.info(f"Listed {len(tasks)} tasks for user: {user_id} with status: {status}")

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ]


def complete_task_service(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Service function to mark a task as completed
    """
    from ..db import SessionLocal

    with SessionLocal() as session:
        # Get the task
        task = session.get(Task, task_id)
        
        # Verify ownership
        if not task or task.user_id != user_id:
            raise ValueError(f"Task {task_id} not found or does not belong to user {user_id}")
        
        # Update completion status
        task.completed = True
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        logger.info(f"Task completed: {task.id} for user: {user_id}")
        
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }


def delete_task_service(user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Service function to delete a task
    """
    from ..db import SessionLocal

    with SessionLocal() as session:
        # Get the task
        task = session.get(Task, task_id)

        # Verify ownership
        if not task or task.user_id != user_id:
            raise ValueError(f"Task {task_id} not found or does not belong to user {user_id}")

        # Delete the task
        session.delete(task)
        session.commit()

        logger.info(f"Task deleted: {task.id} for user: {user_id}")

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title
        }


def edit_task_service(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Service function to edit an existing task
    """
    from ..db import SessionLocal

    with SessionLocal() as session:
        # Get the task
        task = session.get(Task, task_id)

        # Verify ownership
        if not task or task.user_id != user_id:
            raise ValueError(f"Task {task_id} not found or does not belong to user {user_id}")

        # Update task fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        session.add(task)
        session.commit()
        session.refresh(task)

        logger.info(f"Task edited: {task.id} for user: {user_id}")

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }


def get_user_info_service(user_id: str) -> Dict[str, Any]:
    """
    Service function to get user's profile information
    """
    # In a real implementation, this would fetch user data from Better Auth
    # For now, we'll return placeholder data based on the user_id
    # In a real system with Better Auth, we would fetch from their user table

    logger.info(f"Retrieved user info for user: {user_id}")

    # Placeholder implementation - in a real system, this would connect to Better Auth
    # to retrieve the user's email and name
    # For demo purposes, we'll create a realistic response based on user_id
    return {
        "email": f"{user_id}@example.com",  # Would come from auth system
        "name": f"User {user_id.split('-')[0] if '-' in user_id else user_id}"  # Would come from auth system
    }