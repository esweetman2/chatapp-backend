from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from Backend.db import  get_session
from typing import Optional
from Backend.Schemas.AgentSchema import Agent
from Backend.Database.AiUserDatabase import AiUserDatabase



router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/", tags=["Users"])
async def get_user(id: Optional[int] = None, session: Session = Depends(get_session)):
    try:
        _AiUserDatabase = AiUserDatabase(session)
        agent = _AiUserDatabase.get_user(id)
        if agent:
            return agent
        else:
            raise HTTPException(status_code=404, detail= "User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/login/", tags=["Login Users"])
async def login_user(email: str = None, session: Session = Depends(get_session)):
    try:
        _AiUserDatabase = AiUserDatabase(session)
        user = _AiUserDatabase.login_user(email=email)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail= "User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/users/", tags=["Users"])
async def add_user(email: str, display_name: str, session: Session = Depends(get_session)):
    try:
        print(email, display_name)
        _AiUserDatabase = AiUserDatabase(session)
        user = _AiUserDatabase.add_user(email=email, display_name=display_name)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))