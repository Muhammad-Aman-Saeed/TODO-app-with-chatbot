from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timezone

from backend.models import Task as TaskModel
from backend.dependencies import get_current_user, get_db_session
from backend.schemas import TaskCreateRequest as TaskCreateSchema, TaskResponse as TaskReadSchema, TaskUpdateRequest as TaskUpdateSchema, TaskPatchRequest as TaskPatchSchema

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskReadSchema])
def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session),
    status_param: Optional[str] = Query(None, alias="status", regex="^(all|pending|completed)$"),
    sort: Optional[str] = Query(None, regex="^(created|title)$")
):
    """
    Get all tasks for the current user with optional filtering and sorting
    """
    # Build the query to filter tasks by the current user
    query = select(TaskModel).where(TaskModel.user_id == current_user_id)

    # Apply status filter if provided
    if status_param and status_param != "all":
        if status_param == "pending":
            query = query.where(TaskModel.completed == False)
        elif status_param == "completed":
            query = query.where(TaskModel.completed == True)

    # Apply sorting if provided
    if sort == "title":
        query = query.order_by(TaskModel.title)
    elif sort == "created":
        query = query.order_by(TaskModel.created_at.desc())

    # Execute the query
    tasks = db.exec(query).all()
    return tasks


@router.post("/", response_model=TaskReadSchema, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreateSchema,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create a new task for the current user
    """
    # Create a new task instance with the current user's ID
    task = TaskModel(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user_id
    )

    # Add the task to the database
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskReadSchema)
def get_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Get a specific task by ID if it belongs to the current user
    """
    # Query for the task with the given ID and user ID
    task = db.exec(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user_id)
    ).first()

    # Raise 404 if task doesn't exist or doesn't belong to the user
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskReadSchema)
def update_task(
    task_id: int,
    task_update: TaskUpdateSchema,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update a specific task if it belongs to the current user
    """
    # Query for the task with the given ID and user ID
    task = db.exec(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user_id)
    ).first()

    # Raise 404 if task doesn't exist or doesn't belong to the user
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided data
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update the updated_at timestamp
    task.updated_at = datetime.now(timezone.utc)

    # Commit the changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Delete a specific task if it belongs to the current user
    """
    # Query for the task with the given ID and user ID
    task = db.exec(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user_id)
    ).first()

    # Raise 404 if task doesn't exist or doesn't belong to the user
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    db.delete(task)
    db.commit()

    return


@router.patch("/{task_id}/complete", response_model=TaskReadSchema)
def toggle_task_completion(
    task_id: int,
    task_patch: TaskPatchSchema,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Toggle the completion status of a specific task if it belongs to the current user
    """
    # Query for the task with the given ID and user ID
    task = db.exec(
        select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user_id)
    ).first()

    # Raise 404 if task doesn't exist or doesn't belong to the user
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the completion status
    task.completed = task_patch.completed
    task.updated_at = datetime.now(timezone.utc)

    # Commit the changes
    db.add(task)
    db.commit()
    db.refresh(task)

    return task