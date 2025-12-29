from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.MessagesDatabase import MessagesDatabase
from Backend.Agents.AgentBuilder.AgentBuilderService import AgentBuilderService
from pydantic import BaseModel
from fastapi.responses import StreamingResponse


router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/messages", tags=["Messages"])
async def get_message(id: Optional[int] = None, chat_id: Optional[int] = None, session: Session = Depends(get_session)):
    try:
        _MessagesDatabase = MessagesDatabase(session)
        message = _MessagesDatabase.get_message(id)
        if message:
            return message
        else:
            raise HTTPException(status_code=404, detail= "Message not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class ChatMessageRequest(BaseModel):
    agent_id: int
    chat_id: int
    message: str
    role: str
    user_id: int


@router.post("/messages", tags=["Messages"])
async def add_message(chatMessage: ChatMessageRequest, session: Session = Depends(get_session)):
    print(chatMessage)
    try:
        _MessagesDatabase = MessagesDatabase(session)
        message = _MessagesDatabase.add_message(user_id=chatMessage.user_id, agent_id=chatMessage.agent_id, chat_id=chatMessage.chat_id, message=chatMessage.message, role=chatMessage.role)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/messages/agent", tags=["Messages"])
async def send_chat( chatMessage: ChatMessageRequest, session: Session = Depends(get_session)):
    try:
        _AgentBuilderService = AgentBuilderService(
            db_session=session, 
            agent_id=chatMessage.agent_id, 
            chat_id=chatMessage.chat_id, 
            query=chatMessage.message, 
            role=chatMessage.role, 
            user_id=chatMessage.user_id,
            )
        response = _AgentBuilderService.generate_response()
        if response:
            return response
        else:
            raise HTTPException(status_code=404, detail= "No response from Messages.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/messages/agent/stream", tags=["Messages"])
async def send_chat( chatMessage: ChatMessageRequest, session: Session = Depends(get_session)):
    try:
        _AgentBuilderService = AgentBuilderService(
            db_session=session, 
            agent_id=chatMessage.agent_id, 
            chat_id=chatMessage.chat_id, 
            query=chatMessage.message, 
            role=chatMessage.role, 
            user_id=chatMessage.user_id,
            )
        return StreamingResponse(_AgentBuilderService.generate_response_stream(), media_type="text/event-stream")
        # if response:
        #     return response
        # else:
        #     raise HTTPException(status_code=404, detail= "No response from Messages.")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))