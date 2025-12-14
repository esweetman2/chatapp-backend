from sqlmodel import Session, select
from fastapi import HTTPException
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.AgentToolsModel import AgentToolsModel
from Backend.Models.ToolsModel import ToolsModel
from pydantic import BaseModel
from datetime import datetime


class AgentToolsDatabase:
    def __init__(self, db: Session):
        self.db = db    
    
    def get_agent_tool(self, agent_id: Optional[int] = None) -> Optional[AgentToolsModel]:
        """Fetch a agent tool"""
        if agent_id is None:
            return self.db.exec(select(AgentToolsModel)).all()
        agent_tool = self.db.exec(select(AgentToolsModel).where(AgentToolsModel.agent_id == agent_id)).all()
        # print(f"Agent tool fetched: {agent_tool}")
        return agent_tool if agent_tool else None

    def get_tools(self, tool_id: Optional[int] = None) -> Optional[ToolsModel]:
        """Fetch a tool"""
        if tool_id is None:
            return self.db.exec(select(ToolsModel)).all()
        tool = self.db.exec(select(ToolsModel).where(ToolsModel.id == tool_id)).first()
        # print(f"Tool fetched: {tool}")
        return tool if tool else None
