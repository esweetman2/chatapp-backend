from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from datetime import datetime, timezone

# CREATE TABLE agentmemories (
#   id BIGSERIAL PRIMARY KEY,
#   chat_id INT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
#   agent_id INT NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
#   payload JSONB,
#   embedding vector(1536),
#   created_at TIMESTAMPTZ DEFAULT now()
# );

class AgentMemory(SQLModel, table=True):
    __tablename__ = "agentmemory"
    id: int = Field(primary_key=True)
    chat_id: int = Field(foreign_key="chats.id")
    agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
    payload: Dict[str, Any] = Field(sa_column=Column(JSONB))
    embedding: Optional[list[float]] = Field(
        sa_column=Column(Vector(1536))
    )
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # user: Optional["AiUser"] = Relationship(back_populates="agentmemory")
    # messages: List["ChatMessages"] = Relationship(back_populates="agentmemory")
