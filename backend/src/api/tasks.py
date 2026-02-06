from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..models.task import TaskRead, TaskCreate, TaskUpdate
from ..services.task_service import (
    create_task, get_tasks_by_user, get_task_by_id_and_user,
    update_task, delete_task, toggle_task_completion
)
from .dependencies import get_db
from ..services.auth import get_current_user
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[TaskRead])
async def get_tasks(
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all tasks for the current user."""
    tasks = get_tasks_by_user(db_session=db, user_id=current_user_id)
    return tasks


@router.post("/", response_model=TaskRead)
async def create_new_task(
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the current user."""
    new_task = create_task(
        db_session=db,
        task_create=task,
        user_id=current_user_id
    )
    return new_task


@router.put("/{task_id}", response_model=TaskRead)
async def update_existing_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing task for the current user."""
    updated_task = update_task(
        db_session=db,
        task_id=task_id,
        task_update=task_update,
        user_id=current_user_id
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task


@router.delete("/{task_id}")
async def delete_existing_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task for the current user."""
    success = delete_task(
        db_session=db,
        task_id=task_id,
        user_id=current_user_id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion_status(
    task_id: str,
    completed: bool,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle the completion status of a task."""
    updated_task = toggle_task_completion(
        db_session=db,
        task_id=task_id,
        completed=completed,
        user_id=current_user_id
    )
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return updated_task