from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LLMSchema(BaseModel):
    id: int
    model_name: str
    platform: str
    created_date: datetime

    