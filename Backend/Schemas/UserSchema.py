from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional, List
from datetime import datetime, timezone
from db import engine
import time

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True)
    email: str
    display_name: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    chats: List["Chat"] = Relationship(back_populates="user")
    agents: List["Agent"] = Relationship(back_populates="owner")