from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.MessageModel import ChatMessages

class MessagesDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_message(self, id: Optional[int] = None, chat_id: Optional[int] = None) -> Optional[ChatMessages]:
        """Fetch a model"""
        if id is None and chat_id is None:
            all_messages = self.db.exec(select(ChatMessages).order_by(ChatMessages.id.desc())).all()
            return all_messages if all_messages else None
        elif id is None and chat_id is not None:
            message = self.db.exec(select(ChatMessages).where(ChatMessages.chat_id == chat_id).order_by(ChatMessages.id.desc())).all()
            return message if message else None 
        elif id is not None:
            message = self.db.exec(select(ChatMessages).where(ChatMessages.id == id)).first()
            return message if message else None
        
        message = self.db.exec(select(ChatMessages).where(ChatMessages.id == id, ChatMessages.chat_id == chat_id)).first()
        # print(f"User fetched: {message}")
        return message if message else None
    
    def add_message(self, user_id: int, agent_id: int, chat_id: int, message: str = None, role: str = None) -> ChatMessages:
        """Add a new model to the database."""
        new_message = ChatMessages( user_id=user_id, agent_id=agent_id, chat_id=chat_id, message=message, role=role)
        self.db.add(new_message)
        self.db.commit()
        self.db.refresh(new_message)
        return new_message