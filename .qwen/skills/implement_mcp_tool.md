# Implement MCP Tool

## Description
Code one MCP tool (e.g., add_task) following specific guidelines for authentication, database operations, and response formatting.

## Guidelines
- Use @app.tool() or FastMCP decorator
- Validate user_id == current_user
- Use SQLModel session for CRUD operations on Task
- Return exact format dict

## Template
```python
# Example implementation for add_task tool
from sqlmodel import Session
from fastmcp import FastMCP
from backend.models import Task
from backend.auth import get_current_user

@app.tool()
def add_task(title: str, description: str = "", user_id: str = None) -> dict:
    """
    Add a new task for the authenticated user.
    
    Args:
        title: The task title
        description: Optional task description
        user_id: The authenticated user's ID
    
    Returns:
        Dictionary with task information
    """
    # Validate that user_id matches authenticated user
    current_user = get_current_user()  # Implementation depends on your auth system
    if user_id != current_user.id:
        raise ValueError("Unauthorized: user_id does not match authenticated user")
    
    # Create task using SQLModel session
    with Session(engine) as session:
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "user_id": task.user_id,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
```

## Output Format
Code snippet with path (e.g., # backend/mcp_tools.py)