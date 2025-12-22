from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from uuid import UUID, uuid4
from datetime import datetime, timezone

# CREATE TABLE chatmessages (
#     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     user_id INTEGER NOT NULL,
#     agent_id INTEGER NOT NULL,
#     chat_id INTEGER NOT NULL,
#     message TEXT NOT NULL,
#     role TEXT NOT NULL,
#     created_date TIMESTAMPTZ NOT NULL DEFAULT now(),

#     CONSTRAINT chatmessages_user_id_fkey
#         FOREIGN KEY (user_id)
#         REFERENCES aiusers(id),

#     CONSTRAINT chatmessages_chat_id_fkey
#         FOREIGN KEY (chat_id)
#         REFERENCES chats(id)
# );

class ChatMessages(SQLModel, table=True):
    __tablename__ = "chatmessages"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="aiusers.id", nullable=False)
    agent_id: Optional[int] = Field(nullable=False)
    chat_id: int = Field(foreign_key="chats.id", nullable=False)
    message: str = Field(nullable=False)
    role: str = Field(nullable=False)  # "user" or "assistant"
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

    # ai_user: Optional["AiUser"] = Relationship(back_populates="chat_messages")
    # agent: Optional["Agent"] = Relationship(back_populates="chat_messages")
    chat: Optional["ChatModel"] = Relationship(back_populates="messages")



    # memories: List["AgentMemory"] = Relationship(back_populates="agentmemory")