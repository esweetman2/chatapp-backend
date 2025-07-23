
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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

user_id = "esweetman"



session = get_session()
config = {
    "vector_store": {
        "provider": "pgvector",
        "config": {
            "user": "chatbotuser",
            "password": "chatbotuser",
            "host": "127.0.0.1",
            "port": "5432",
            "dbname": "chatbotDb"
        }
    }
}


# m = Memory()
memory = Memory.from_config(config)
# print(memory.__dict__)


def test_vector():


    messages = [
    {"role": "user", "content": "I'm planning to watch a movie tonight. Any recommendations?"},
    {"role": "assistant", "content": "How about a thriller movies? They can be quite engaging."},
    {"role": "user", "content": "I'm not a big fan of thriller movies but I love sci-fi movies."},
    {"role": "assistant", "content": "Got it! I'll avoid thriller recommendations and suggest sci-fi movies in the future."}
]
    
    result = memory.add(messages, user_id="esweetman", metadata={"category": "movie_recommendations"})

    print(result)

    # response = client.responses.create(
    #     model="gpt-4o",
    #     tools=[{ "type": "web_search_preview" }],
    #     input="Who won the 2025 PGA The Open?",
    # )

    # print(response.output[1].content[0].text)
    return

# test_vector()

all_memories = memory.get_all(user_id="esweetman")
# print(all_memories)

related_memories = memory.search(query="What do you know about me?", user_id="esweetman")
print()
print(related_memories["results"])

for i in related_memories["results"]:
    print(i["memory"], "\n")
