from sqlmodel import SQLModel, Field, Relationship, Column
from typing import Optional, List, Dict, Any
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from datetime import datetime, timezone

# CREATE TABLE agentmemory (
#     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     agent_id INTEGER REFERENCES agents(id),
#     user_id INTEGER REFERENCES aiusers(id),
#     memory_text TEXT NOT NULL,
#     embedding VECTOR(1536),
#     created_date TIMESTAMPTZ NOT NULL DEFAULT NOW()
# );

class AgentMemory(SQLModel, table=True):
    __tablename__ = "agentmemory"
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: Optional[int] = Field(default=None, foreign_key="agents.id")
    user_id: Optional[int] = Field(default=None, foreign_key="aiusers.id")
    
    # payload: Dict[str, Any] = Field(sa_column=Column(JSONB))
    memory_text: str = Field(nullable=False)
    embedding: Optional[list[float]] = Field(
        sa_column=Column(Vector(1536))
    )
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # user: Optional["AiUser"] = Relationship(back_populates="agentmemory")
    # messages: List["ChatMessages"] = Relationship(back_populates="agentmemory")
