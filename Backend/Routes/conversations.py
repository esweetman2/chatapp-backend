from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter
from sqlmodel import SQLModel, Session
from Backend.Routes import users
from Backend.Models.models import Conversation, Message
from Backend.memory import get_or_create_conversation, get_conversation_messages, add_message, check_convo, get_conversation, get_conversations
from Backend.db import engine, get_session
from pydantic import BaseModel
from Backend.Schemas.schemas import ChatRequest, ChatResponse, NewConversationRequest, GenericReturn
from fastapi.middleware.cors import CORSMiddleware
import tiktoken
from Helpers.convertPydantic import convert_pydantic_to_dict

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(tags=["Conversations"])

# Load OpenAI API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@router.get("/conversation")
def get_convo( id: int, user_id: str, session: Session = Depends(get_session)):
    # Create a new conversation
    print(type(id), id)
    # conversation = get_or_create_conversation(session, request.user_id, request.id)
    conversation = get_conversation(db=session, conversation_id=id, user_id=user_id)
    print("Conversation:", conversation)
    # convo = conversation[0]["conversation"]
    # messages = conversation[0]["messages"]
    
    if conversation is None:
        return "Not Found"
    # if conversation[0]["conversation"].id is not None:
        # return "Convo Not found"
    return [{"conversation" : conversation, "messages": conversation.messages}]

@router.get("/conversations")
def get_convos( user_id: str, session: Session = Depends(get_session)):
    conversations = get_conversations(db=session, user_id=user_id)
    # print("Conversations:", conversations)  

    if conversations is None:
        return "Not Found"
    return conversations

@router.post("/newchat", response_model=NewConversationRequest)
def new_chat(request: NewConversationRequest, session: Session = Depends(get_session)):
    # Create a new conversation
    conversation = get_or_create_conversation(session, request.user_id, request.id)
    convo = conversation[0]["conversation"]
    messages = conversation[0]["messages"]

    if conversation[0]["conversation"].id is not None:
        return NewConversationRequest(id=convo.id, user_id=convo.user_id, messages=messages)
    return "Error creating conversation"

# @router.post("/newchat/title", response_model=ChatResponse)
# def add_title_to_chat(request: ChatRequest, session: Session = Depends(get_session)):
#     return ChatResponse(response="Generic Response",  convo_id=request.convo_id, user_id=request.user_id, messages=[])

