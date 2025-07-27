
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
            "user": "postgres",
            "password": "$Hockeylax2",
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
    
    system_message = {"role": "system", "content": "You're an expert programmer that helps build applications."}
    
    while True:
        
        user_input = input("Write here: ")
        if user_input.lower() == "exit":
            print("Breaking loop......")
            break
        messages = [system_message]
        
        related_memories = memory.search(query=user_input, user_id="esweetman")
#           print(i["memory"], "\n")
        print(related_memories)
        for i in related_memories["results"]:
            print("printing memory.....")
            print(i)
            messages.append({"role": "user", "content": i["memory"]})
            print()
            
        messages.append({"role": "user", "content": user_input})
        

        
        memory.add(user_input, user_id="esweetman")
        # all_memories = memory.get_all(user_id="esweetman")

        # print(result)
        # print(messages)
        # break

        response = client.responses.create(
            model="gpt-4o",
            tools=[{ "type": "web_search_preview" }],
            input=messages,
        )

        res = response.output_text
        print()
        print(res)
        print()
        
        memory.add(res, user_id="esweetman")
        
    return

test_vector()

# all_memories = memory.get_all(user_id="esweetman")
# # print(all_memories)

# related_memories = memory.search(query="What do you know about me?", user_id="esweetman")
# print()
# print(related_memories["results"])

# for i in related_memories["results"]:
#     print(i["memory"], "\n")
