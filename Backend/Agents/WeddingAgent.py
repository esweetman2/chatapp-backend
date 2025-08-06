
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

class WeddingAgent:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()
# user_id = "esweetman"
# session = get_session()
        self.config = {
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
        self.memory = Memory.from_config(self.config)
        self.system_message ='''
        You're an expert AI assistant who's goal is to provide as much detail as possible for a wedding.
        
        1. You MUST return revelant details about the users query.
        2. You MUST return any timeline details with timestamps if possible.
        3. You MUST use the revelant memories for context to give the best precise answer.
        4. If you need more clarification then ask the user to add the details so you have more context.
        5. If the user asks anything about location and addresses you can utlize the web to look for answers.
        
        '''
        
    def related_memories(self, user_input):
        related_memories = self.memory.search(query=user_input, user_id=self.user_id)
        return related_memories
    
    def add_memories(self, user_input):
        self.memory.add(user_input, user_id=self.user_id)
        print("Memory added.")
    
    def handle_messages(self, memories: list, user_input: str):
        messages = [{"role": "system", "content": self.system_message}]
        for i in memories["results"]:
            messages.append({"role": "user", "content": i["memory"]})
        
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def get_all_messages(self):
        all_memories = self.memory.get_all(user_id=self.user_id)
        return all_memories
    
    def handle_LLM(self, messages: list):
        response = client.responses.create(
            model="gpt-4o",
            tools=[{ "type": "web_search_preview" }],
            input=messages
        )

        res = response.output_text
        return res
        
def main():
    _WeddingAgent = WeddingAgent("esweetman")
    
    while True:
        user_input = input("User Input: ")
        if user_input.lower() == "exit":
            print("Breaking loop......")
            break
        
        _WeddingAgent.add_memories(user_input=user_input)
        
        related_messages = _WeddingAgent.related_memories(user_input=user_input)
        input_messages = _WeddingAgent.handle_messages(memories=related_messages, user_input=user_input)
        
        # print(input_messages)
        
        llm_output = _WeddingAgent.handle_LLM(input_messages)
        print("\n=============== Wedding Agent Repsonse ============\n")
        print(llm_output)
        print("")

if __name__ == "__main__":
    # main()
    _weddingAgent = WeddingAgent("esweetman")
    # all_memories = _weddingAgent.get_all_messages()
    # print(all_memories)
    # print(len(all_memories["results"]))
    print()
    search = _weddingAgent.related_memories("What time does the wedding ceremony start?")
    # print(search)
    
    for i in search["results"]:
        if i["score"] >= .8:
            print(i)
            print()
    # print(len(search["results"]))
    
    
    
    