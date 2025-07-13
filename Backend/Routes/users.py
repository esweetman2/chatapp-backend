from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import  Session
from db import  get_session
from schemas import User
from ..Database.usersService import UsersService

router = APIRouter()


# @router.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/user/", tags=["users"], response_model=User)
async def get_user(username: str, session: Session = Depends(get_session)):
    _userService = UsersService(session)
    user = _userService.get_user(username)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail= "User not found")


# @router.get("/users/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}