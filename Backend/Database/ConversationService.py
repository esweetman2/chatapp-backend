from sqlmodel import Session, select
from Backend.Models.models import Conversation, Message, Users
from db import engine
from typing import Optional
from schemas import User

class ConversationService:
    def __init__(self, db: Session):
        self.db = db
    
    # def get_conversation(self, _username: str) -> Optional[User]:
    #     """Fetch a user by username."""
    #     user = self.db.exec(select(Users).where(Users.username == _username)).first()
    #     print(f"User fetched: {user}")
    #     return user if user else None