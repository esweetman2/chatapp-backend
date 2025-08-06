
# from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
# from models import Conversation, Message
from memory import get_or_create_conversation, get_conversation_messages, add_message, updateConversatinSummary
from db import engine, get_session
# from pydantic import BaseModel
from schemas import ChatRequest, ChatResponse
import os
import json
from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# query = "Will Kat and Eric's dog be at the wedding?"
# query_embedding = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=query
# ).data[0].embedding

# print(query_embedding)

# query = "name is bob."
# query_embedding = client.embeddings.create(
#     model="text-embedding-3-small",
#     input=query
# ).data[0].embedding

# print(query_embedding)