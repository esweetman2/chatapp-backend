from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.ChatModel import ChatModel

class ChatsDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_chat(self, id: Optional[int] = None) -> Optional[ChatModel]:
        """Fetch a model"""
        if id is None:
            all_chats = self.db.exec(select(ChatModel)).all()
            return all_chats if all_chats else None
        model = self.db.exec(select(ChatModel).where(ChatModel.id == id)).first()
        print(f"User fetched: {model}")
        return model if model else None
    
    def add_chat(self, user_id: id, agent_id:int , title: Optional[str] = None) -> ChatModel:
        """Add a new model to the database."""
        new_chat = ChatModel( user_id=user_id, agent_id=agent_id, title=title)
        self.db.add(new_chat)
        self.db.commit()
        self.db.refresh(new_chat)
        return new_chat