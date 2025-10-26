from sqlmodel import Session, select
from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
from Backend.Schemas.schemas import User

class UsersService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user(self, _username: str) -> Optional[User]:
        """Fetch a user by username."""
        user = self.db.exec(select(Users).where(Users.username == _username)).first()
        print(f"User fetched: {user}")
        return user if user else None