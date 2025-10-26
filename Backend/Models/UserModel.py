from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional, List
from datetime import datetime, timezone

class AiUser(SQLModel, table=True):
    __tablename__ = "aiusers"
    id: int = Field(primary_key=True)
    email: str
    display_name: Optional[str] = None
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # chats: List["Chat"] = Relationship(back_populates="aiusers")
    chat_messages: List["ChatMessages"] = Relationship(back_populates="ai_user")
    # agents: List["Agent"] = Relationship(back_populates="agents")