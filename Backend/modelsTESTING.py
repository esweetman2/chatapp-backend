from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional, List
from datetime import datetime, timezone
from Backend.db import engine
import time

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    title: str = Field(default=None)
    summary: Optional[str] = None  # Summary of the conversation    
    messages: List[Message] = Relationship(back_populates="conversation")

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# SQLModel.metadata.create_all(engine)
# print(Conversation(user_id = "12345adsf"))
# Message.conversation = Relationship(back_populates="messages", sa_relationship_kwargs={"lazy": "selectin"})

# with Session(engine) as session:
#     # session.exec(text("ALTER TABLE conversation ADD summary TEXT;"))
#     # session.commit()
#     user = Users(username="kpayne")
#     print(user)
#     session.add(user)
#     session.commit()
    # session.add(Users(username="esweetman"))
    # session.commit()
    # session.refresh(conversation)
    # print(conversation.id, conversation.user_id, conversation.created_at)
    # print("Tables created successfully.")