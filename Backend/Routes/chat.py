from typing import Annotated
from fastapi import FastAPI, Depends, APIRouter
from sqlmodel import SQLModel, Session
from Backend.Routes import users
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
router = APIRouter(tags=["Chat"])

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



@router.post("/newchat/systemmessage",response_model=ChatResponse)
def new_chat(request: ChatRequest, session: Session = Depends(get_session)):
    # Create a new conversation
    # 
    print(request)
    return ChatResponse(response="Generic Response",  cono_id=request.convo_id, user_id=request.user_id, messages=[])

    # if conversation[0]["conversation"].id is not None:
    #     return NewConversationRequest(id=convo.id, user_id=convo.user_id, messages=messages)
    return "Error creating conversation"

@router.post("/chat", response_model=ChatResponse)
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
        message_inputs = convert_pydantic_to_dict(messages)
    
    # Add user message to the conversation 
    user_message = {"role": "user", "content": request.message.strip()}
    message_inputs.append(user_message)
       
    if len(message_inputs) > 10: 
        sliced_messages = message_inputs[-10:]
        sliced_messages.insert(0, message_inputs[0])
        message_inputs = sliced_messages

    # return ChatResponse(response="Generic Response",  cono_id=request.convo_id, user_id=request.user_id, messages=message_inputs) 
    # Add user message to the database
    add_message(session, convo[0]["conversation"].id, user_message["role"], user_message["content"])


    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    # enc = tiktoken.encoding_for_model("gpt-4o")
    total_tokens = 0
    
    for message in message_inputs:
        for key in message:
            msg = None
            if key == "content":
                msg = message[key].strip()
                enc = tiktoken.encoding_for_model("gpt-4o")
                encoded_tokens = enc.encode(msg.strip())
                total_tokens += len(encoded_tokens)
                
    ## Need to figure out how to manage too many tokens
    if total_tokens >= 100000:
        return ChatResponse(response="Token Limit too high",  cono_id=request.convo_id, user_id=request.user_id, messages=message_inputs)   
    print(f"\nTotal Token are: {total_tokens}")
    # encoded_tokens = enc.encode(request.message.strip())

    # Send to OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o",
        input=message_inputs,
        store=False  # Set to True if you want OpenAI to retain conversation
    )

    # Parse the response
    reply = response.output[0].content[0].text

    # Add assistant reply to the conversation in database
    add_message(session, convo[0]["conversation"].id, "assistant", reply)

    return ChatResponse(response=reply,  cono_id=request.convo_id, user_id=request.user_id, messages=message_inputs)