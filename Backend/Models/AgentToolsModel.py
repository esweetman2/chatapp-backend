from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
# from uuid import UUID, uuid4
from datetime import datetime, timezone


# CREATE TABLE agent_tools (
#     agent_id INT REFERENCES agents(id) ON DELETE CASCADE,
#     tool_id INT REFERENCES tools(id) ON DELETE CASCADE,
#     PRIMARY KEY (agent_id, tool_id)
# );

class AgentToolsModel(SQLModel, table=True):
    __tablename__ = "agenttools"
    agent_id: int = Field(foreign_key="agents.id", primary_key=True, nullable=False)
    tool_id: int = Field(foreign_key="tools.id", primary_key=True, nullable=False)

