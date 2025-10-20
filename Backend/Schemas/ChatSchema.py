from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Chat(SQLModel, table=True):
    __tablename__ = "chats"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id")
    agent_id: Optional[UUID] = Field(default=None, foreign_key="agents.id")
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="chats")
    messages: List["Message"] = Relationship(back_populates="chat")
    memories: List["Memory"] = Relationship(back_populates="chat")
