'''

This is a wedding agent with preconfigured memory.

The memory needs to be managed outside the Agent

'''



from openai import OpenAI
from pydantic import BaseModel, Field
import os
from typing import Literal, List
from dotenv import load_dotenv
from Backend.db import engine, Session
from Backend.Agents.WeddingAgent.WeddingMemory import MemoryMangement
from memory import add_message, get_conversation_messages
load_dotenv()

class WeddingAgent2:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._weddingMangement = MemoryMangement()

    def get_memories(self, query):
        try:
            memories = self._weddingMangement.search_memory(query=query, memory_table="weddingmemory",top_k=5)
            return memories
        except Exception as e:
            print("Exception", e)
            
    def store_memory(self, memory: str):
        return self._weddingMangement.store_memory(memory)
        
        #   2. question: This is a question asked by the user. 
        # Use this query to run the analysis {query}.      
    def _system_prompt(self, memories):
        prompt = f'''
        You're an AI assistant that MUST answer questions regarding a wedding.
        
        Use these memories to help your response. {str(memories)}
        
        '''
        return prompt
    
    def _generate_input(self,query, system_prompt):
        inputs = [
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query,
            },
        ]
        return inputs
        
        
    def generate_response(self, inputs):
        response = self.client.responses.parse(
            model="gpt-4o",
            input=inputs,
            tools=[{ "type": "web_search_preview" }],
            store=False,
        )

        llm_response = response.output_text
        # print(response)
        return llm_response
    
if __name__ == "__main__":
    
    agent = WeddingAgent2()
    
    while True:
        query = input("User Query: ")
        print("\n")
        
        with Session(engine) as session:
            conversation_history = get_conversation_messages(session,1)
            # print(conversation_history)
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        if query.lower() == "exit":
            print("Exiting Agent...")
            break
        
        memories = agent.get_memories(query=query)

        system_prompt = agent._system_prompt( memories=memories)

        inputs = agent._generate_input(query=query, system_prompt=system_prompt)
        
        if len(conversation_history) != 0:
            for input_index in range(len(conversation_history)):
                _insert_input = {"role": conversation_history[input_index].role, "content": conversation_history[input_index].content}
                inputs.insert(input_index + 1, _insert_input)
        
        response = agent.generate_response(inputs=inputs)
        
        with Session(engine) as session:
            add_message(session, 1, "user", query)
            add_message(session, 1, "assistant", response)

        print(response, "\n")


