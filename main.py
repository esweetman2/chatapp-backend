from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from Backend.Routes import users
from models import Conversation, Message
from memory import get_or_create_conversation, get_conversation_messages, add_message, check_convo, get_conversation, get_conversations
from db import engine, get_session
from pydantic import BaseModel
from schemas import ChatRequest, ChatResponse, NewConversationRequest, GenericReturn
from fastapi.middleware.cors import CORSMiddleware
import tiktoken

import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
app.include_router(users.router)

origins = ["*"]

app.add_middleware(
        CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)
@app.get("/conversation")
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

@app.get("/conversations")
def get_convos( user_id: str, session: Session = Depends(get_session)):
    conversations = get_conversations(db=session, user_id=user_id)

    if conversations is None:
        return "Not Found"
    return conversations

@app.post("/newchat", response_model=NewConversationRequest)
def new_chat(request: NewConversationRequest, session: Session = Depends(get_session)):
    # Create a new conversation
    conversation = get_or_create_conversation(session, request.user_id, request.id)
    convo = conversation[0]["conversation"]
    messages = conversation[0]["messages"]

    if conversation[0]["conversation"].id is not None:
        return NewConversationRequest(id=convo.id, user_id=convo.user_id, messages=messages)
    return "Error creating conversation"


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)):


    ## Check if conversation exists
    ## If exists, good we will use it
    convo = check_convo(session, request.convo_id, request.user_id)
    if not convo:
        return ChatResponse(response="Unable to find conversation.", cono_id=request.convo_id, user_id=request.user_id)
    
    # Get conversation messages
    messages = convo[0]["messages"]

    ## Initialize chat messages inputs
    message_inputs = []

    ### check if messages is empty list ###
    if messages == []: # if empty, start new message chain with system message
        system_message = {"role": "system", "content": "You are an expert AI assistant."}
        message_inputs.append(system_message)
        add_message(session, convo[0]["conversation"].id, system_message["role"], system_message["content"])
    else: # Use existing messages
        message_inputs = messages.copy()

    # Add user message to the conversation 
    user_message = {"role": "user", "content": request.message.strip()}
    message_inputs.append(user_message)

    # Add user message to the database
    add_message(session, convo[0]["conversation"].id, user_message["role"], user_message["content"])


    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    # enc = tiktoken.encoding_for_model("gpt-4o")
    total_tokens = 0
    for message in message_inputs:
        for key in message:
            if key == "content":
                print(message[key].strip())
                # Encode the content to count tokens
                # enc = tiktoken.encoding_for_model("gpt-4o")
                # encoded_tokens = enc.encode(message[key].strip())
                # total_tokens += len(encoded_tokens)
            # print(f"Key: {key}, Value: {message[key]}")

    # encoded_tokens = enc.encode(request.message.strip())




    return ChatResponse(response="reply",  cono_id=request.convo_id, user_id=request.user_id, messages=message_inputs)
    # Send to OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o",
        input=message_inputs,
        store=False  # Set to True if you want OpenAI to retain conversation
    )

    # Parse the response
    reply = response.output[0].content[0].text

    # Add assistant reply to the conversation in database
    add_message(session, convo.id, "assistant", reply)
