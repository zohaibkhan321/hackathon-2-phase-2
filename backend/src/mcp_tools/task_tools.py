from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from sqlalchemy import desc
from ..models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ..models.user import User
from datetime import datetime


async def add_task(db: Session, user_id: UUID, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Add a new task for the user."""
    task_data = TaskCreate(title=title, description=description)
    task = Task(**task_data.dict(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


async def list_tasks(db: Session, user_id: UUID) -> List[Dict[str, Any]]:
    """List all tasks for the user."""
    from sqlalchemy import desc
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db.exec(statement).all()
    
    return [
        {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        for task in tasks
    ]


async def complete_task(db: Session, user_id: UUID, task_id: str) -> Dict[str, Any]:
    """Mark a task as completed."""
    task = db.get(Task, UUID(task_id))
    if not task or task.user_id != user_id:
        raise ValueError("Task not found or access denied")
    
    task.completed = True
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }


async def delete_task(db: Session, user_id: UUID, task_id: str) -> bool:
    """Delete a task."""
    task = db.get(Task, UUID(task_id))
    if not task or task.user_id != user_id:
        raise ValueError("Task not found or access denied")
    
    db.delete(task)
    db.commit()
    return True


async def update_task(db: Session, user_id: UUID, task_id: str, **kwargs) -> Dict[str, Any]:
    """Update a task."""
    task = db.get(Task, UUID(task_id))
    if not task or task.user_id != user_id:
        raise ValueError("Task not found or access denied")
    
    # Update allowed fields
    if "title" in kwargs and kwargs["title"]:
        task.title = kwargs["title"]
    if "description" in kwargs:
        task.description = kwargs["description"]
    if "completed" in kwargs:
        task.completed = kwargs["completed"]
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    return {
        "id": str(task.id),
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }