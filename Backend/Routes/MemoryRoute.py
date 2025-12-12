from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.AgentDatabase import AgentDatabase
# from ..Database.usersService import UsersService
# from Backend.Database.usersService import UsersService


router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


# @router.get("/memory", tags=["Memory"])
# async def get_agent(id: Optional[int] = None, session: Session = Depends(get_session)):
#     try:
#         _AgentDatabase = AgentDatabase(session)
#         agent = _AgentDatabase.get_agent(id)
#         if agent:
#             return agent
#         else:
#             raise HTTPException(status_code=404, detail= "Agent not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# @router.post("/memory", tags=["Memory"])
# async def create_agent(agent_name: str, description: str, model: str, model_id: int, system_message:str, session: Session = Depends(get_session)):
#     try:
#         _AgentDatabase = AgentDatabase(session)
#         agent = _AgentDatabase.add_agent(agent_name=agent_name, description=description, model=model, model_id=model_id, system_message=system_message)
#         return agent
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))