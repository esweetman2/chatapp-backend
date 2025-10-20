from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from uuid import UUID, uuid4
from datetime import datetime, timezone

class AgentChatMessagesMomory(SQLModel, table=True):
    __tablename__ = "chatmessages"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional["User"] = Relationship(back_populates="chats")
    messages: List["Message"] = Relationship(back_populates="chat")
    memories: List["Memory"] = Relationship(back_populates="chat")