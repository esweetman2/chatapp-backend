from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from uuid import UUID, uuid4
from datetime import datetime, timezone

class ChatMessages(SQLModel, table=True):
    __tablename__ = "chatmessages"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="aiusers.id", nullable=False)
    agent_id: Optional[int] = Field(nullable=False, foreign_key="agents.id")
    title: Optional[str] = None
    message: str = Field(nullable=False)
    role: str = Field(nullable=False)  # "user" or "assistant"
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    ai_user: Optional["AiUser"] = Relationship(back_populates="chat_messages")
    agent: Optional["Agent"] = Relationship(back_populates="chat_messages")
    # chat: List["ChatMessages"] = Relationship(back_populates="chat")



    # memories: List["AgentMemory"] = Relationship(back_populates="agentmemory")