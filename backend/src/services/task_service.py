from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


def create_task(*, db_session: Session, task_create: TaskCreate, user_id: str) -> Task:
    """Create a new task for a user."""
    task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def get_tasks_by_user(*, db_session: Session, user_id: str) -> List[Task]:
    """Get all tasks for a specific user."""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db_session.exec(statement).all()
    return tasks


def get_task_by_id_and_user(*, db_session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a specific user."""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db_session.exec(statement).first()
    return task


def update_task(*, db_session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
    """Update a task for a user."""
    task = get_task_by_id_and_user(db_session=db_session, task_id=task_id, user_id=user_id)
    if not task:
        return None

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


def delete_task(*, db_session: Session, task_id: str, user_id: str) -> bool:
    """Delete a task for a user."""
    task = get_task_by_id_and_user(db_session=db_session, task_id=task_id, user_id=user_id)
    if not task:
        return False

    db_session.delete(task)
    db_session.commit()
    return True


def toggle_task_completion(*, db_session: Session, task_id: str, completed: bool, user_id: str) -> Optional[Task]:
    """Toggle the completion status of a task."""
    task = get_task_by_id_and_user(db_session=db_session, task_id=task_id, user_id=user_id)
    if not task:
        return None

    task.completed = completed
    task.updated_at = datetime.utcnow()
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task

