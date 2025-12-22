from sqlmodel import Session, select
# from Backend.Models.models import Conversation, Message, Users
from Backend.db import engine
from typing import Optional
# from Backend.Schemas.schemas import User
# from Backend.Schemas.AgentSchema import Agent
from Backend.Models.LLMModel import LLMModel

class LLMModelDatabase:
    def __init__(self, db: Session):
        self.db = db
    
    def get_model(self, id: Optional[int] = None) -> Optional[LLMModel]:
        """Fetch a model"""

        if id is None:
            all_models = self.db.exec(select(LLMModel)).all()
            return all_models if all_models else None
        model = self.db.exec(select(LLMModel).where(LLMModel.id == id)).first()
        # print(f"User fetched: {model}")
        return model if model else None
    
    def add_model(self, model_name: str, platform: str) -> LLMModel:
        """Add a new model to the database."""
        new_model = LLMModel( model_name= model_name, platform=platform)
        self.db.add(new_model)
        self.db.commit()
        self.db.refresh(new_model)
        return new_model