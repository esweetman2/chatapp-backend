from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.LLMModelSchema import LLMSchema
from Backend.Database.LLMModelDatabase import LLMModelDatabase


router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/llmmodel/", tags=["LLM Model"])
async def get_model(id: Optional[int] = None, session: Session = Depends(get_session)):
    _LLMModelDatabase = LLMModelDatabase(session)
    agent = _LLMModelDatabase.get_model(id)
    if agent:
        return agent
    else:
        raise HTTPException(status_code=404, detail= "Model not found")

@router.post("/llmmodel/", tags=["LLM Model"])
async def create_model(model_name: str, platform: str, session: Session = Depends(get_session)):
    _LLMModelDatabase = LLMModelDatabase(session)
    model = _LLMModelDatabase.add_model(model_name=model_name, platform=platform)
    return model