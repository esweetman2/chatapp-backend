from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.MemoryDatabase import MemoryDatabase
from pydantic import BaseModel
# from ..Database.usersService import UsersService
# from Backend.Database.usersService import UsersService


router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/memory", tags=["Memory"])
async def search_memory( query: str, top_k: int, agent_id: int, session: Session = Depends(get_session)):
    try:
        _MemoryDatabase = MemoryDatabase(session)
        memory = _MemoryDatabase.search_memory(query=query, memory_table="agentmemory", agent_id=agent_id, top_k=top_k)
        print(memory)
        if memory or memory == []:
            return str(memory)
        else:
            raise HTTPException(status_code=404, detail= "Agent not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PostMemory(BaseModel):
    memory_text: str
    user_id: int
    agent_id: int

@router.post("/memory", tags=["Memory"])
async def store_memory( postMemory: PostMemory, session: Session = Depends(get_session)):
    try:
        _MemoryDatabase = MemoryDatabase(session)
        memory = _MemoryDatabase.store_memory(memory_text=postMemory.memory_text, user_id=postMemory.user_id, agent_id=postMemory.agent_id)
        return memory
        if memory or memory == []:
            return memory
        else:
            raise HTTPException(status_code=404, detail= "Memory not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))