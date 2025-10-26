from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.ChatsDatabase import ChatsDatabase



router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/chats/", tags=["Chats"])
async def get_chat(id: Optional[int] = None, session: Session = Depends(get_session)):
    try:
        _ChatsDatabase = ChatsDatabase(session)
        agent = _ChatsDatabase.get_chat(id)
        if agent:
            return agent
        else:
            raise HTTPException(status_code=404, detail= "Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chats/", tags=["Chats"])
async def add_chat(user_id: int, agent_id: int, title: Optional[str] = None, session: Session = Depends(get_session)):
    try:
        _ChatsDatabase = ChatsDatabase(session)
        user = _ChatsDatabase.add_chat(user_id=user_id, agent_id=agent_id, title=title)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))