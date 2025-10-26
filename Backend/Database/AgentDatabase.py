from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.AgentModel import Agent

class AgentDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_agent(self, id: Optional[int] = None) -> Optional[Agent]:
        """Fetch a agent"""
        if id is None:
            return self.db.exec(select(Agent)).all()
        agent = self.db.exec(select(Agent).where(Agent.id == id)).first()
        print(f"Agent fetched: {agent}")
        return agent if agent else None
    
    def add_agent(self, agent_name: str, description: str, model: str, model_id: int, system_message: str) -> Agent:
        """Add a new agent to the database."""
        new_agent = Agent(agent_name=agent_name, description=description, model=model, model_id=model_id, system_message=system_message)
        self.db.add(new_agent)
        self.db.commit()
        self.db.refresh(new_agent)
        return new_agent