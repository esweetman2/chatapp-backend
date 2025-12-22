from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from fastapi import HTTPException
from Backend.Models.ChatModel import ChatModel
from pydantic import BaseModel
from datetime import datetime

class ChatRepsonse(BaseModel):
    id: int
    agent_id: int
    title: str
    created_date: datetime
    summary: str
    message_start_index: int

class ChatsDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_chat(self, id: Optional[int] = None, user_id: Optional[int] = None, agent_id: Optional[int] = None):
        """Fetch a model"""
        # print(user_id, agent_id)
        if id is None and user_id is None:
            # print("id is None and user_id is None")
            all_chats = self.db.exec(select(ChatModel).order_by(ChatModel.created_date.desc())).all()
            return all_chats if all_chats else None
        
        elif id is not None:
            # print("id is not None")
            chat = self.db.exec(select(ChatModel).where(ChatModel.id == id)).first()
            return chat if chat else None
        
        elif user_id is not None and agent_id is not None:
            # print("user_id is not None and agent_id is not None")
            chat = self.db.exec(select(ChatModel).where(ChatModel.user_id == user_id).where(ChatModel.agent_id == agent_id).order_by(ChatModel.created_date.desc())).all()
            return chat if chat else None
        
        elif user_id is not None:
            # print("user_id is not None:")
            chats = self.db.exec(select(ChatModel).where(ChatModel.user_id == user_id).order_by(ChatModel.created_date.desc()).order_by(ChatModel.created_date.desc())).all()
            return chats if chats else None
        
        
        else:
            return None
    
    def add_chat(self, user_id: id, agent_id:int , title: Optional[str] = None) -> ChatModel:
        """Add a new model to the database."""
        new_chat = ChatModel( user_id=user_id, agent_id=agent_id, title=title)
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat
    
    def update_chat(self, updates: ChatModel) -> ChatModel:
        try:
            
            chat = self.db.get(ChatModel, updates.id)

            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            # 2. Extract updates data, excluding the ID if it's present in the response model
        #    and excluding any unset values if using a PATCH approach
            del updates.messages
            update_data = updates.model_dump(exclude_unset=True)


            # 3. Update the existing chat object's attributes using a loop
            for key, value in update_data.items():
                setattr(chat, key, value)

            self.db.add(chat)
            self.db.commit()
            self.db.refresh(chat)

            return chat
        except Exception as e:
            print("DATABASE FAILED")
            return HTTPException(status_code=500, detail=str(e))