from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, timezone

class ChatModel(SQLModel, table=True):
    __tablename__ = "chats"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="aiusers.id")
    agent_id: int = Field(default=None, foreign_key="agents.id")
    title: Optional[str] = None
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # aiuser: Optional["AiUser"] = Relationship(back_populates="chats")
    # chat: List["ChatModel"] = Relationship(back_populates="chat")
    # memories: List["AgentMemory"] = Relationship(back_populates="agentmemory")
