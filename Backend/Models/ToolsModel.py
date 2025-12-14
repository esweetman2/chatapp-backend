from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy import Column
# from uuid import UUID, uuid4
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB

# CREATE TABLE agenttools (
#     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     tool_type TEXT NOT NULL,            -- web_search_preview | function
#     name TEXT,                          -- NULL for non-function tools
#     description TEXT,
#     parameters JSONB,                   -- function schema
#     enabled BOOLEAN DEFAULT TRUE,
#     created_at TIMESTAMP DEFAULT NOW(),
#     CONSTRAINT unique_tool UNIQUE (tool_type, name)
# );


class ToolsModel(SQLModel, table=True):
    __tablename__ = "tools"
    id: Optional[int] = Field(default=None, primary_key=True)
    tool_type: str = Field(nullable=False)            # web_search_preview | function
    name: Optional[str] = None                          # NULL for non-function tools
    description: Optional[str] = None
    parameters: Optional[dict] = Field(
        default=None,
        sa_column=Column(JSONB)             # <-- explicitly define JSONB
    )                 # function schema
    enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
