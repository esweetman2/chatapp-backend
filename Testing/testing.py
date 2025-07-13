
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
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

user_id = "12345adsf"



session = get_session()

# convo = get_or_create_conversation(session, user_id)

# print(convo[0].id, convo[0].user_id, convo[0].created_at)
# for i in convo[1]:
#     print(i.id, i.role, i.content, i.timestamp)
# msg = add_message(session, conversation_id, "TESTER", "This is a test")

def chat(request: ChatRequest, session: Session = Depends(get_session)):
    # Load/create conversation
    conversation = get_or_create_conversation(session, request.user_id, request.id)
    convo = conversation[0]["conversation"]
    messages = conversation[0]["messages"]
    print("Messages:", messages)
    print("Convo:", convo)
    return

    # return convo
    history = [{"role": m.role, "content": m.content} for m in convo[1]]
    print(history)
    if history == []:
        system_message = {"role": "system", "content": "You are an expert assistant. You MUST return a summary of the chat history in a field called summary. Within your response you MUST return a JSON object of `{`summary: <summary of chat history>, text: <your response text>`}`. You MUST return a valid JSON string"}
        history.append(system_message)
    print(history)

    
    # Save user's message
    add_message(session, convo[0].id, "user", user_input)
    
    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if( user_input.lower() == 'exit'):
            print("Exiting chat.")
            return
        
        # print("User: ", user_input)
        history.append({"role": "user", "content": user_input})
        print("History: ", history)
        
        response = client.responses.create(
            model="gpt-4o",
            input=history,
            # previous_response_id=convo.last_response_id,
            store=False  # Set to True if you want OpenAI to retain conversation
        )

        reply = response.output[0].content[0].text
        res_dict = json.loads(reply)
        print(res_dict)
        updateSum = updateConversatinSummary(session, convo[0].id, res_dict['summary'])
        print(updateSum.summary)
        # print(res_dict['summary'])
        # print(res_dict['text'])

    return


    # Send to OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o",
        input=request.message,
        # previous_response_id=convo.last_response_id,
        store=False  # Set to True if you want OpenAI to retain conversation
    )

    reply = response.output[0].content[0].text

    print("Reply from OpenAI:", reply)
    return

    # Save assistant reply
    add_message(session, convo.id, "assistant", reply)

    # Update response_id for conversation state
    convo.last_response_id = response.id
    session.add(convo)
    session.commit()

    return ChatResponse(response=reply)

chatReq = ChatRequest(user_id=user_id, message="Hello, how are you?", id=3)
chat(chatReq, session)

