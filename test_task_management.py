"""
Test script to verify all task management functionalities work correctly.
This includes add, complete, delete, and edit tasks through the chatbot interface.
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.services.task_service import (
    add_task_service,
    list_tasks_service,
    complete_task_service,
    delete_task_service,
    edit_task_service
)

def test_task_management():
    print("Testing Task Management Functions...")
    
    # Mock user ID for testing
    test_user_id = "test-user-123"
    
    # Test 1: Add a task
    print("\n1. Testing add_task_service...")
    try:
        result = add_task_service(
            user_id=test_user_id,
            title="Test Task",
            description="This is a test task"
        )
        task_id = result["task_id"]
        print(f"[SUCCESS] Successfully added task with ID: {task_id}")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to add task: {e}")
        return

    # Test 2: List tasks
    print("\n2. Testing list_tasks_service...")
    try:
        tasks = list_tasks_service(user_id=test_user_id)
        print(f"[SUCCESS] Successfully listed tasks. Found {len(tasks)} task(s)")
        for task in tasks:
            print(f"  - Task ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
    except Exception as e:
        print(f"[ERROR] Failed to list tasks: {e}")
        return

    # Test 3: Edit the task
    print("\n3. Testing edit_task_service...")
    try:
        result = edit_task_service(
            user_id=test_user_id,
            task_id=task_id,
            title="Updated Test Task",
            description="This is an updated test task"
        )
        print(f"[SUCCESS] Successfully edited task with ID: {task_id}")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to edit task: {e}")
        return

    # Test 4: Complete the task
    print("\n4. Testing complete_task_service...")
    try:
        result = complete_task_service(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"[SUCCESS] Successfully marked task as completed: {task_id}")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to complete task: {e}")
        return

    # Test 5: List tasks again to see the updated status
    print("\n5. Testing list_tasks_service after completion...")
    try:
        tasks = list_tasks_service(user_id=test_user_id)
        print(f"[SUCCESS] Successfully listed tasks after completion. Found {len(tasks)} task(s)")
        for task in tasks:
            print(f"  - Task ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
    except Exception as e:
        print(f"[ERROR] Failed to list tasks after completion: {e}")
        return

    # Test 6: Edit the task again (to uncomplete it)
    print("\n6. Testing edit_task_service to uncomplete task...")
    try:
        result = edit_task_service(
            user_id=test_user_id,
            task_id=task_id,
            completed=False
        )
        print(f"[SUCCESS] Successfully edited task completion status: {task_id}")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to edit task completion status: {e}")
        return

    # Test 7: Delete the task
    print("\n7. Testing delete_task_service...")
    try:
        result = delete_task_service(
            user_id=test_user_id,
            task_id=task_id
        )
        print(f"[SUCCESS] Successfully deleted task: {task_id}")
        print(f"  Result: {result}")
    except Exception as e:
        print(f"[ERROR] Failed to delete task: {e}")
        return

    # Test 8: List tasks again to confirm deletion
    print("\n8. Testing list_tasks_service after deletion...")
    try:
        tasks = list_tasks_service(user_id=test_user_id)
        print(f"[SUCCESS] Successfully listed tasks after deletion. Found {len(tasks)} task(s)")
        if len(tasks) == 0:
            print("  [SUCCESS] Task was successfully deleted")
        else:
            for task in tasks:
                print(f"  - Task ID: {task['id']}, Title: {task['title']}, Completed: {task['completed']}")
    except Exception as e:
        print(f"[ERROR] Failed to list tasks after deletion: {e}")
        return

    print("\n[SUCCESS] All task management functions tested successfully!")


def test_error_cases():
    print("\n\nTesting Error Cases...")
    
    # Test error case: trying to access a non-existent task
    print("\n1. Testing access to non-existent task...")
    try:
        result = complete_task_service(
            user_id="non-existent-user",
            task_id=99999  # Assuming this task ID doesn't exist
        )
        print(f"✗ Should have failed to access non-existent task, but got: {result}")
    except Exception as e:
        print(f"[SUCCESS] Correctly failed to access non-existent task: {e}")

    # Test error case: trying to edit a non-existent task
    print("\n2. Testing edit of non-existent task...")
    try:
        result = edit_task_service(
            user_id="non-existent-user",
            task_id=99999,  # Assuming this task ID doesn't exist
            title="New Title"
        )
        print(f"[ERROR] Should have failed to edit non-existent task, but got: {result}")
    except Exception as e:
        print(f"[SUCCESS] Correctly failed to edit non-existent task: {e}")


if __name__ == "__main__":
    test_task_management()
    test_error_cases()
    print("\n\n[SUCCESS] All tests completed!")