from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional
from datetime import datetime, timezone
from db import engine
import time


class Agent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_name: str = Field(unique=True)
    system_message: str
    agent_type: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model: str

class LLM_Models(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str = Field(unique=True)
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

SQLModel.metadata.create_all(engine)
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