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
    # Load/create conversation
    # conversation = get_or_create_conversation(session, request.user_id, request.id)
    # print(conversation)
    # convo = conversation[0]["conversation"]
    # messages = conversation[0]["messages"]
    
    convo = check_convo(session, request.convo_id, request.user_id)
    # Save user's message
    # add_message(session, request.convo_id, "user", request.message)
    print(convo)
    if not convo:
        return ChatResponse(response="Unable to find conversation.")
    
    summary = convo.summary
    if summary is None:
        system_message = {"role": "system", "content": "You are an expert assistant. You MUST return a summary of the chat history in a field called summary. Within your response you MUST return a JSON object of `{`summary: <summary of chat history>, text: <your response text>`}`. You MUST return a valid JSON string"}
        # history.append(system_message)
        summary = [system_message]
    print(summary)
    return ChatResponse(response="Message saved successfully.")
    # Send to OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o",
        input=request.message,
        previous_response_id=convo.last_response_id,
        store=False  # Set to True if you want OpenAI to retain conversation
    )

    reply = response.output[0].content[0].text

    # Save assistant reply
    add_message(session, convo.id, "assistant", reply)

    # Update response_id for conversation state
    convo.last_response_id = response.id
    session.add(convo)
    session.commit()

    return ChatResponse(response=reply)