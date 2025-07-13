from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic schemas
class ChatRequest(BaseModel):
    user_id: str
    convo_id: int
    message: str
    id: Optional[int] = None  # Optional conversation ID for existing conversations

class ChatResponse(BaseModel):
    response: str

class NewConversationRequest(BaseModel):
    user_id: str
    id: int | None = None  # Optional conversation ID for existing conversations
    messages: Optional[list] = None  # Optional list of messages for the new conversation

class User(BaseModel):
    id: int
    username: str 
    created_at: datetime # ISO format date string

class GenericReturn(BaseModel):
    error: bool
    message: str