from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship, Session, text
from datetime import datetime, timezone


class LLMModel(SQLModel, table=True):
    __tablename__ = "llmmodels"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_name: str = Field(nullable=False, unique=True)
    platform: str
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    output_tokens: int = Field(nullable=False)
    context_window: int = Field(nullable=False)
    