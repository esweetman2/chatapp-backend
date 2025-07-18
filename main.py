from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from Backend.Routes import users, conversations, chat
from models import Conversation, Message
from memory import get_or_create_conversation, get_conversation_messages, add_message, check_convo, get_conversation, get_conversations
from db import engine, get_session
from pydantic import BaseModel
from schemas import ChatRequest, ChatResponse, NewConversationRequest, GenericReturn
from fastapi.middleware.cors import CORSMiddleware
import tiktoken
from Helpers.convertPydantic import convert_pydantic_to_dict

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
origins = ["*"]

app.add_middleware(
        CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(chat.router)



# Create database tables
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)
