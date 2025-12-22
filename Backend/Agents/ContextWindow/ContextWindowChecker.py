import tiktoken
from openai import OpenAI
from pydantic import BaseModel, Field
import os
from typing import Literal, List
from dotenv import load_dotenv
from Backend.db import engine
from sqlmodel import Session
import json
# from db import engine, Session
# from Backend.Agents.WeddingAgent.WeddingMemory import MemoryMangement
# from memory import add_message, get_conversation_messages
import json
from Backend.Database.AgentDatabase import AgentDatabase
from Backend.Database.ChatsDatabase import ChatsDatabase
from Backend.Database.MessagesDatabase import MessagesDatabase
from Backend.Database.MemoryDatabase import MemoryDatabase
from Backend.Database.AgentToolsDatabase import AgentToolsDatabase
from Backend.Agents.Tools.GoogleSheets import GoogleSheets
from Backend.Database.LLMModelDatabase import LLMModelDatabase




class ContextWindowChecker:
    def __init__(self, db_session, agent_id: int, agent_model: str, model_id: int, messages: list):
        self.agent_id = agent_id
        self.agent_model = agent_model
        self.model_id = model_id
        self.messages = messages
        self.llm_models = LLMModelDatabase(db=db_session)
        self.messages = messages

    def _get_tokens_used(self, messages):
        encoding = tiktoken.encoding_for_model(self.agent_model)

        token_ids = encoding.encode(messages)
        return len(token_ids)

    def _get_llm_agent_details(self):
        llm_model_details = self.llm_models.get_model(self.model_id)
        return llm_model_details
    
    def _check_context_window(self, messages: list):

        total_tokens = self._get_tokens_used(messages=json.dumps(messages))
        llm_model_details = self._get_llm_agent_details()
        output_tokens = llm_model_details.output_tokens
        context_window = llm_model_details.context_window

        threshold = context_window - output_tokens

        if total_tokens > threshold:
            return True

        return False
    def manage_context_window(self):
        check_context_window = self._check_context_window(self.messages)
        return check_context_window


# if __name__ == "__main__":
#     messages = [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Hello!"},
#         {"role": "assistant", "content": "Hi there! How can I assist you today?"},
#         # Add more messages as needed for testing
#     ] * 10000  # Replicate to increase token count
#     print(len(messages))
#     with Session(engine) as session:
#         context_manager = ContextWindowChecker(db_session=session, agent_id=2, agent_model="gpt-4o", model_id=1, messages=messages)

#         res = context_manager.manage_context_window()
#         print(res)