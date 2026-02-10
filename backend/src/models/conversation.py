from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
from .user import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task


class ConversationBase(SQLModel):
    pass


class Conversation(ConversationBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    user_id: UUID


class ConversationRead(ConversationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class MessageBase(SQLModel):
    role: str  # "user" or "assistant"
    content: str


class Message(MessageBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    conversation_id: UUID


class MessageRead(MessageBase):
    id: UUID
    conversation_id: UUID
    created_at: datetime


class ChatMessage(SQLModel):
    message: str


class ChatResponse(SQLModel):
    response: str
    tool_results: Optional[List[dict]] = None
    conversation_id: Optional[UUID] = None