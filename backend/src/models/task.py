from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None