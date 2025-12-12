'''

This is class for constructing agents to do functionality.


'''



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
from Backend.Database.AgentDatabase import AgentDatabase
from Backend.Database.ChatsDatabase import ChatsDatabase
from Backend.Database.MessagesDatabase import MessagesDatabase
load_dotenv()

class AgentBuilderService:
    def __init__(self, db_session, agent_id: int, chat_id: int, query: str = "", role: str = "user", user_id: int = None):
        self.db_session = db_session
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agent = AgentDatabase(db_session).get_agent(agent_id)
        self.chat_id = chat_id
        self.role = role
        self.query = query
        self.user_id = user_id
        self._MessagesDatabase = MessagesDatabase(self.db_session)
        if not self.agent:
            raise ValueError(f"Agent with id={agent_id} not found")
        
        self.agent_id = agent_id
        self.agent_name = self.agent.agent_name
        self.description = self.agent.description
        self.system_message = self.agent.system_message
        self.agent_model = self.agent.model   
    
    def test_agent(self):
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "description": self.description,
            "system_message": self.system_message,
            "agent_model": self.agent_model
        }
    def _get_message_history(self):
        messages = self._MessagesDatabase.get_message(chat_id=self.chat_id)
        if messages:
            message_list = []
            for message in messages:
                message_list.append({
                    "role": message.role,
                    "content": message.message
                })
            return message_list
        return []
    
    def _generate_input(self):
        inputs = [
            {
                "role": "system", 
                "content": self.system_message
            },
        ]
        messages = self._get_message_history()
        for message in messages:
            inputs.append({
                "role": message['role'],
                "content": message['content'],
            })
        inputs.append({
            "role": self.role,
            "content": self.query
        })

        return inputs
    
    def _store_message(self, role: str, content: str):
        # _MessageDatabase = MessagesDatabase(self.db_session)
        add_message = self._MessagesDatabase.add_message(
            user_id=self.user_id,
            agent_id=self.agent_id,
            chat_id=self.chat_id,
            message=content,
            role=role
        )
        return add_message

    
    def generate_response(self):

        try:
            inputs = self._generate_input()
            # print(inputs)
            response = self.client.responses.parse(
                model=self.agent_model,
                input=inputs,
                tools=[{ "type": "web_search_preview" }],
                store=False,
            )

            self._store_message(role=self.role, content=self.query)
            agent_response = self._store_message(role="assistant", content=response.output_text)

        except Exception as e:
            print("Error storing agent response: ", str(e))
            agent_response = None
        
        return agent_response
    
# if __name__ == "__main__":
#     messages = []
#     with Session(engine) as session:

#         agent = AgentBuilderService(session, agent_id=4, chat_id=1, query="What is your purpose?", role="user", user_id=1)

#         response = agent.generate_response()
#         print("Agent Response: ", response)





    
#     agent = WeddingAgent2()
    
#     while True:
#         query = input("User Query: ")
#         print("\n")
        
#         with Session(engine) as session:
#             conversation_history = get_conversation_messages(session,1)
#             # print(conversation_history)
#         if len(conversation_history) > 10:
#             conversation_history = conversation_history[-10:]
        
#         if query.lower() == "exit":
#             print("Exiting Agent...")
#             break
        
#         memories = agent.get_memories(query=query)

#         system_prompt = agent._system_prompt( memories=memories)

#         inputs = agent._generate_input(query=query, system_prompt=system_prompt)
        
#         if len(conversation_history) != 0:
#             for input_index in range(len(conversation_history)):
#                 _insert_input = {"role": conversation_history[input_index].role, "content": conversation_history[input_index].content}
#                 inputs.insert(input_index + 1, _insert_input)
        
#         response = agent.generate_response(inputs=inputs)
        
#         with Session(engine) as session:
#             add_message(session, 1, "user", query)
#             add_message(session, 1, "assistant", response)

#         print(response, "\n")


