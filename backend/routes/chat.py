"""
Chat Route Module

This module implements the POST /api/chat endpoint with Cohere integration.
It handles the complete chat flow: authentication, conversation management,
Cohere API calls with tool usage, and response handling.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional, List
import cohere
from sqlmodel import Session, select
from datetime import datetime
import os
from ..dependencies import get_current_user
from ..models import Conversation, Message
from ..tools.cohere_tools import COHERE_TOOLS, execute_add_task, execute_list_tasks, execute_complete_task, execute_delete_task, execute_edit_task, execute_get_user_info, AddTaskArgs, ListTasksArgs, CompleteTaskArgs, DeleteTaskArgs, EditTaskArgs, GetUserInfoArgs
from pydantic import BaseModel

router = APIRouter()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if cohere_api_key:
    cohere_client = cohere.Client(api_key=cohere_api_key)
else:
    # For development/testing without Cohere API key
    cohere_client = None
    print("Warning: COHERE_API_KEY not set. Chat functionality will not work.")


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None


class TaskData(BaseModel):
    id: str = ""
    title: str = ""
    description: str = ""
    completed: bool = False


class ChatActionResponse(BaseModel):
    action: str  # "add", "delete", "update", "complete", "list", "none"
    task: Optional[TaskData] = None
    message: str
    conversation_id: int


@router.post("/chat", response_model=ChatActionResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user)
):
    """
    Main chat endpoint that integrates with Cohere API for natural language processing
    and returns responses in the required JSON format for task management.
    """
    from ..db import SessionLocal

    session = SessionLocal()
    try:
        # Step 1: Get or create conversation
        if request.conversation_id:
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")

            # Verify user owns the conversation
            if conversation.user_id != current_user_id:
                raise HTTPException(status_code=403, detail="Access denied to this conversation")
        else:
            # Create new conversation
            conversation = Conversation(user_id=current_user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Step 2: Save user message to Message table
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Step 3: Load last 20-30 messages (ordered by created_at) → format as Cohere chat history
        # Get recent messages for context
        recent_messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
            .limit(30)  # Limit to last 30 messages for context
        ).all()

        # Format messages for Cohere
        chat_history = []
        for msg in recent_messages:
            chat_history.append({
                "role": "USER" if msg.role == "user" else "CHATBOT",
                "message": msg.content
            })

        # Step 4: Call cohere.chat with tools
        if cohere_api_key is None:
            # Return a mock response when Cohere is not available
            from ..utils.mock_responses import get_mock_chat_response
            response = get_mock_chat_response(request.message)
        else:
            try:
                response = cohere_client.chat(
                    model="command-r-plus",
                    message=request.message,
                    chat_history=chat_history[:-1],  # Exclude the current message
                    tools=COHERE_TOOLS,
                    force_single_step=False  # Allow multi-step tool use
                )
            except Exception as e:
                # If there's an error with Cohere API, fall back to mock response
                print(f"Cohere API error: {str(e)}, falling back to mock response")
                from ..utils.mock_responses import get_mock_chat_response
                response = get_mock_chat_response(request.message)

        # Step 5: Handle tool calls and map to required action format
        action = "none"
        task_data = None
        response_message = ""

        if hasattr(response, 'tool_calls') and response.tool_calls:
            # Process the first tool call to determine the action
            first_tool_call = response.tool_calls[0]
            tool_name = first_tool_call.name
            tool_args = first_tool_call.parameters

            # Execute the appropriate tool based on its name and map to action
            try:
                if tool_name == "add_task":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = AddTaskArgs(**tool_args_for_execution)
                    result = execute_add_task(args_model, current_user_id)
                    action = "add"
                    task_data = TaskData(
                        id=str(result.get("task_id", "")),
                        title=tool_args.get("title", ""),
                        description=tool_args.get("description", ""),
                        completed=False
                    )
                    response_message = result.get("status", "Task added successfully")

                elif tool_name == "list_tasks":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = ListTasksArgs(**tool_args_for_execution)
                    result = execute_list_tasks(args_model, current_user_id)
                    action = "list"
                    response_message = f"Found {len(result)} tasks"

                elif tool_name == "complete_task":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = CompleteTaskArgs(**tool_args_for_execution)
                    result = execute_complete_task(args_model, current_user_id)
                    action = "complete"
                    task_data = TaskData(
                        id=str(tool_args.get("task_id", "")),
                        title=result.get("title", ""),
                        completed=True
                    )
                    response_message = result.get("status", "Task completed")

                elif tool_name == "delete_task":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = DeleteTaskArgs(**tool_args_for_execution)
                    result = execute_delete_task(args_model, current_user_id)
                    action = "delete"
                    task_data = TaskData(
                        id=str(tool_args.get("task_id", ""))
                    )
                    response_message = result.get("status", "Task deleted")

                elif tool_name == "edit_task":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = EditTaskArgs(**tool_args_for_execution)
                    result = execute_edit_task(args_model, current_user_id)
                    action = "update"
                    task_data = TaskData(
                        id=str(tool_args.get("task_id", "")),
                        title=tool_args.get("title", result.get("title", "")),
                        description=tool_args.get("description", result.get("description", "")),
                        completed=tool_args.get("completed", result.get("completed", False))
                    )
                    response_message = result.get("status", "Task updated")

                elif tool_name == "get_user_info":
                    # Override user_id in tool_args with authenticated user ID for security
                    tool_args_for_execution = {**tool_args, "user_id": current_user_id}
                    args_model = GetUserInfoArgs(**tool_args_for_execution)
                    result = execute_get_user_info(args_model, current_user_id)
                    action = "none"
                    response_message = f"User info: {result.get('name', 'Unknown')} ({result.get('email', 'No email')})"

                else:
                    action = "none"
                    response_message = f"Unknown tool: {tool_name}"

            except Exception as e:
                action = "none"
                response_message = f"Error executing tool: {str(e)}"
        else:
            # No tool calls were made, return a general response
            action = "none"
            response_message = response.text if hasattr(response, 'text') else str(response)

        # Step 6: Save assistant message to Message table
        # Use the response message that's appropriate for the action
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=response_message
        )
        session.add(assistant_message)
        session.commit()

        # Update conversation's updated_at timestamp
        from datetime import datetime, timezone
        conversation.updated_at = datetime.now(timezone.utc)
        session.add(conversation)
        session.commit()

        # Step 7: Return response in required format
        response_obj = ChatActionResponse(
            action=action,
            task=task_data,
            message=response_message,
            conversation_id=conversation.id
        )
    finally:
        session.close()

    return response_obj


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_history(
    conversation_id: int,
    current_user_id: str = Depends(get_current_user)
):
    """
    Retrieve the message history for a specific conversation
    """
    from ..db import SessionLocal

    session = SessionLocal()
    try:
        # Verify user owns the conversation
        conversation = session.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

        if conversation.user_id != current_user_id:
            raise HTTPException(status_code=403, detail="Access denied to this conversation")

        # Get all messages for this conversation
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()

        # Format messages for response
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            })

        return formatted_messages
    finally:
        session.close()


# System prompt for Cohere (defined as a constant)
SYSTEM_PROMPT = """You are an intelligent, state-aware Todo Assistant chatbot integrated inside a Todo web application.
Your responses must be in JSON format with these fields: action, task, message.
Actions can be: add, delete, update, complete, list, none.
For task-related actions, populate the task object with id, title, description, completed.
For list action, task can be null.
For none action, task must be null.
Never respond with plain text for task actions.
Examples:
For "Add buy milk" -> {"action": "add", "task": {"id": "", "title": "buy milk", "description": "", "completed": false}, "message": "Added buy milk task"}
For "Show tasks" -> {"action": "list", "task": null, "message": "Here are your tasks"}
For "Hello" -> {"action": "none", "task": null, "message": "Hello! How can I help with your tasks?"}
Always respond in the required JSON format."""