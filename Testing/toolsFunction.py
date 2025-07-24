
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
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

# user_id = "12345adsf"
# session = get_session()
def get_current_time():
    return datetime.now(timezone.utc)

tools = [{
    "type": "function",
    "name": "get_current_time",
    "description": "Returning the current time",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
            # "additionalProperties": False
        },
        # "strict": True
}]

def call_function(name):
    if name == "get_current_time":
        return get_current_time()
    # if name == "send_email":
    #     return send_email(**args)

def testTool():
    input_messages = [{"role": "user", "content": "What is the current time in EST New York."}]
    # input_messages = [{"role": "user", "content": "Write me python code for adding 2 numbers."}]
    
    response = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools,
        store=False 
    )

    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)
        print("Function called:", name, args)

        result = call_function(name)
        print("Function result:", result)

        # 👇 Full context passed here
        input_messages.append( {
                "type": "function_call",
                "call_id": tool_call.call_id,
                "name": tool_call.name,
                "arguments": tool_call.arguments
            })
        input_messages.append(            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result)
            })
        print(input_messages)

        response2 = client.responses.create(
            model="gpt-4o",
            input=input_messages,
            tools=tools,
        )

        print("Final assistant response:\n", response2.output_text)
        return
    print(response.output_text)

testTool() 
# x = get_current_time()
# print(type(x))   