from sqlmodel import SQLModel, Field, Relationship, Session, text
from typing import Optional, List
from datetime import datetime, timezone
from Backend.db import engine
import time


class Agent(SQLModel, table=True):
    __tablename__ = "agents"
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_name: str = Field(unique=True)
    description: Optional[str] = None
    system_message: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model: str = Field(nullable=False)
    model_id: int = Field(nullable=False)
    use_memory: bool

    # chat_messages: List["ChatMessages"] = Relationship(back_populates="agent")




    

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