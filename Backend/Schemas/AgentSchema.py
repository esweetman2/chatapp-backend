from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Agent(BaseModel):
    id: int
    agent_name: str
    system_message: str
    agent_type: str
    created_date: datetime
    model: str
    model_id: int



    # __tablename__ = "agents"
    # id: Optional[int] = Field(default=None, primary_key=True)
    # agent_name: str = Field(unique=True)
    # system_message: str
    # agent_type: str
    # created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    # model: str
