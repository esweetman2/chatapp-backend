from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.ChatsDatabase import ChatsDatabase
from pydantic import BaseModel
from datetime import datetime, timezone




router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


class ChatModel(BaseModel):
    id: Optional[int] = None
    user_id: int
    agent_id: int 
    title: Optional[str] = None
    created_date: Optional[datetime] = None
    messages: Optional[list] = []   
    summary: Optional[str] = None
    message_start_index: Optional[int] = 0

@router.get("/chats", tags=["Chats"])
async def get_chat(id: Optional[int] = None, user_id: Optional[int] = None, agent_id: Optional[int] = None, session: Session = Depends(get_session)) -> ChatModel | list[ChatModel]:
    try:
        _ChatsDatabase = ChatsDatabase(session)
        chat = _ChatsDatabase.get_chat(id, user_id, agent_id)
        if chat or chat == []:
            return chat
        elif chat == None:
            return []
        else:
            raise HTTPException(status_code=404, detail= "Chat not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# @router.post("/chats/", tags=["Chats"])
# async def add_chat(user_id: int, agent_id: int, title: Optional[str] = None, session: Session = Depends(get_session)):
#     try:
#         _ChatsDatabase = ChatsDatabase(session)
#         user = _ChatsDatabase.add_chat(user_id=user_id, agent_id=agent_id, title=title)
#         return user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chats", tags=["Chats"])
async def add_chat(newChat: ChatModel, session: Session = Depends(get_session)):
    try:
        # print(newChat)
        _ChatsDatabase = ChatsDatabase(session)
        new_chat = _ChatsDatabase.add_chat(user_id=newChat.user_id, agent_id=newChat.agent_id, title=newChat.title)
        # print(newChat)
        return new_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/chats", tags=["Put Chats"])
async def update_chat(updates: ChatModel, session: Session = Depends(get_session)):
    try:
        _ChatsDatabase = ChatsDatabase(session)
        chat = _ChatsDatabase.update_chat(updates=updates)
        return chat
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @router.post("/chatsreqbody/", tags=["Chats Request Body"])
# async def add_chat(item: ChatModel, session: Session = Depends(get_session)):
#     return item
    # try:
    #     _ChatsDatabase = ChatsDatabase(session)
    #     user = _ChatsDatabase.add_chat(user_id=user_id, agent_id=agent_id, title=title)
    #     return user
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))