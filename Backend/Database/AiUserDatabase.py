from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.UserModel import AiUser

class AiUserDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, id: Optional[int] = None) -> Optional[AiUser]:
        """Fetch a model"""
        if id is None:
            all_users = self.db.exec(select(AiUser)).all()
            return all_users if all_users else None
        user = self.db.exec(select(AiUser).where(AiUser.id == id)).first()
        print(f"User fetched: {user}")
        return user if user else None
    
    def add_user(self, email: str, display_name: str) -> AiUser:
        print(email, display_name, "DATABASE")
        """Add a new model to the database."""
        new_user = AiUser( email=email, display_name=display_name)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user