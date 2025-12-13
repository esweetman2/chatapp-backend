from sqlmodel import Session, select
from fastapi import HTTPException
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.AgentModel import Agent
from pydantic import BaseModel
from datetime import datetime

class AgentResponse(BaseModel):
    id: int
    agent_name: str
    description: str
    system_message: str
    created_date: datetime
    updated_date: datetime
    model: str
    model_id: int
    use_memory: bool
    
class AgentDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_agent(self, id: Optional[int] = None) -> Optional[Agent]:
        """Fetch a agent"""
        if id is None:
            return self.db.exec(select(Agent)).all()
        agent = self.db.exec(select(Agent).where(Agent.id == id)).first()
        # print(f"Agent fetched: {agent}")
        return agent if agent else None
    
    def add_agent(self, agent_name: str, description: str, model: str, model_id: int, system_message: str) -> Agent:
        """Add a new agent to the database."""
        new_agent = Agent(agent_name=agent_name, description=description, model=model, model_id=model_id, system_message=system_message)
        self.db.add(new_agent)
        self.db.commit()
        self.db.refresh(new_agent)
        return new_agent
    
    def update_agent(self, agent_id: int, updates: AgentResponse) -> Agent:
        """Update an agent using a dictionary of fields."""
        try:
            agent = self.db.get(Agent, agent_id)
            
            if not agent:
                raise HTTPException(status_code=404, detail="Agent not found")

            # 2. Extract updates data, excluding the ID if it's present in the response model
        #    and excluding any unset values if using a PATCH approach
            update_data = updates.model_dump(exclude_unset=True)

            # 3. Update the existing agent object's attributes using a loop
            for key, value in update_data.items():
                setattr(agent, key, value)

                self.db.add(agent)
                self.db.commit()
                self.db.refresh(agent)

            return agent
        except Exception as e:
            return HTTPException(status_code=500, detail=str(e))