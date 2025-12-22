from openai import OpenAI
from pydantic import BaseModel, Field
import os
from typing import Literal, List
from dotenv import load_dotenv
from Backend.db import engine
from sqlmodel import Session
# from db import engine, Session
# from Backend.Agents.WeddingAgent.WeddingMemory import MemoryMangement
# from memory import add_message, get_conversation_messages
import json
from Backend.Database.AgentDatabase import AgentDatabase
from Backend.Database.LLMModelDatabase import LLMModelDatabase
# from Backend.Agents.AgentBuilder.ContextWindowChecker import ContextWindowManager
from datetime import datetime
# from Backend.Database.ChatsDatabase import ChatsDatabase
# from Backend.Database.MessagesDatabase import MessagesDatabase
# from Backend.Database.MemoryDatabase import MemoryDatabase
# from Backend.Database.AgentToolsDatabase import AgentToolsDatabase


class LLMModel(BaseModel):
    id: int
    model_name: str
    platform: str
    created_at: str
class AgentResponse(BaseModel):
    id: int
    agent_name: str
    description: str
    system_message: str
    created_date: datetime
    updated_date: datetime
    model: str
    model_id: int
    use_memory: bool

class AgentList(BaseModel):
    agents: List[AgentResponse]

class SummarizationAgent:
    def __init__(self, db_session, messages: list):
        self.db_session = db_session
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        # self.agent = AgentDatabase(db_session).get_agent(agent_id)
        self.llm_model = LLMModelDatabase(db_session)
        self.agents = AgentDatabase(db_session)
        self.messages = messages

    
    def _get_summarization_agent(self):
        _agents = self.agents.get_agent()

        summarization_agent = None
        for i in _agents:
            if i.agent_name == "Summarization Agent":
                summarization_agent = i 

        return summarization_agent.model_dump()
        
    
    def generate_summarization_messages(self ) -> str:
        """Generate a summarization prompt based on the agent's system message and recent messages."""
        
        summarization_agent = self._get_summarization_agent()
        print(summarization_agent)
        print("\n")
        # summarization_model = self._get_summarization_model(summarization_agent["model_id"])
        # print(summarization_model)
        system_message = summarization_agent["system_message"]
        # print(system_message)
        self.messages.insert(0, { "role": "assistant", "content": system_message})
        print(self.messages[-1])
        self.messages = self.messages[0:-10]
        print(self.messages)
        print(len(self.messages))

        llm_response = self.client.responses.parse(
            model=summarization_agent["model"],
            input=messages,
            store=False,
        )

        return llm_response.output_text

if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I assist you today?"},
        # Add more messages as needed for testing
    ]   # Replicate to increase token count

    with Session(engine) as session:
        _SummarizationAgent = SummarizationAgent(db_session=session, messages=messages)
        # _agent = _SummarizationAgent.

        llm_output = _SummarizationAgent.generate_summarization_messages()
        print(llm_output)
        # llm_db = LLMModelDatabase(session)
        # models = llm_db.get_model()
        # print("LLM Models in DB:", models)
        



        