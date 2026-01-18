from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.AgentDatabase import AgentDatabase
from pydantic import BaseModel
from datetime import datetime
# from ..Database.usersService import UsersService
# from Backend.Database.usersService import UsersService


router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/agent", tags=["agent"])
async def get_agent(id: Optional[int] = None, session: Session = Depends(get_session)):
    try:
        _AgentDatabase = AgentDatabase(session)
        agent = _AgentDatabase.get_agent(id)
        if agent or agent == []:
            return agent
        else:
            raise HTTPException(status_code=404, detail= "Agent not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AgentRequest(BaseModel):
    id: Optional[int] = None
    agent_name: str
    description: str
    system_message: str
    model: str
    model_id: int
    use_memory: bool

@router.post("/agent", tags=["agent"])
async def create_agent(newAgent: AgentRequest, session: Session = Depends(get_session)):
    try:
        _AgentDatabase = AgentDatabase(session)
        agent = _AgentDatabase.add_agent(agent_name=newAgent.agent_name, description=newAgent.description, model=newAgent.model, model_id=newAgent.model_id, system_message=newAgent.system_message)
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    
    
      
@router.put("/agent", tags=["agent"])
async def put_agent(agent_id: int, updates: AgentResponse, session: Session = Depends(get_session)):
    try:
        _AgentDatabase = AgentDatabase(session)
        agent = _AgentDatabase.update_agent(agent_id=agent_id, updates=updates)
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))