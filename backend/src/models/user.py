# src/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import Column, String

if TYPE_CHECKING:
    from .task import Task
    from .conversation import Conversation, Message

class UserBase(SQLModel):
    email: str = Field(index=True, nullable=False)

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # 🔥 THIS IS REQUIRED
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")

class UserCreate(SQLModel):
    email: str
    password: str

class UserRead(SQLModel):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime
