from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from Backend.Routes import ChatRoute, users, conversations, chat, AgentRoute, LLMModelRoute, AiUserRoute
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
# app.include_router(users.router)
# OLD ROUTES
# app.include_router(conversations.router)
# app.include_router(chat.router)

# NEW ROUTES
app.include_router(AiUserRoute.router)
app.include_router(AgentRoute.router)
app.include_router(LLMModelRoute.router)
app.include_router(ChatRoute.router)




# Create database tables
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)
