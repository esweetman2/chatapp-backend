from openai import OpenAI
from pydantic import BaseModel, Field
import os
from typing import Literal, List
from dotenv import load_dotenv
from db import engine, Session
from Backend.Agents.WeddingAgent.WeddingMemory import MemoryMangement
from memory import add_message, get_conversation_messages
load_dotenv()


class FactResponse(BaseModel):
    fact_summary: str
    response: str
    category: Literal["fact","duplicate", "update", "other"]
    memory: List[str] = Field(..., description="A list of relevant memories or pieces of information associated with the fact including the memory id.")
    reason: str
    
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
        # prompt = f'''
        # your an AI asssistant for a wedding and you MUST extract information from the user's question and your responses to classify it as a fact or other. You MUST only classify the query a **fact** if it is related to a wedding or information about activities or restaurants around the wedding venue, but still provide a response even if the user query has nothing to do with the wedding.
        
        # If the user's input is a fact you MUST generate a clasified_text string that structures the information in fact summary to later be retrieved with similarity search for context. 
        
        # Use this query to run the analysis {query}. 
        
        # **Use these definitions to classify as fact, qusestion, or other:**
        # 1. fact: this is a fact about our wedding. If the user query is a question and your response generates facts, you MUST extract factual information that can help you learn more about the wedding and categorize those facts. (e.g. close restaurants, close activities, venue information, cermony and reception times, etc.)

        # 2. other: This has nothing to do with our wedding. Answer the query as normal.
        
        # 3. fact_summary: Generate a summary of facts about the wedding's information.  (e.g. close restaurants, close activities, venue information, cermony and reception times, etc.)
        
        # You these memories to help your response. {str(memories)}
        
        # Can you return an explaination in the reason field as to why you didn't add the restaurants to the fact_summary?
        # '''
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
            # text_format=FactResponse,
            store=False,
            # stream=True
        )

        llm_response = response.output_text
        return llm_response
    
    def llm_summary(self, txt: str, memories: list):
        sys_prompt = f'''
        Generate a summary of factual information from the following text \n\n {txt}
        
        # **Use these definitions to classify as fact or other:**
        1. fact: this is a fact about our wedding. If the user query is a question and your response generates facts, you MUST extract factual information that can help you learn more about the wedding and categorize those facts. (e.g. close restaurants, close activities, venue information, cermony and reception times and addresses, etc.).
        
        2. Duplicate: This is if you find a similar memory you must return the memory that it is duplicated against.
        
        3. Update: This is if a memory that needs to be updated with a full name  or full address or if anything changes. Look for information within the query gives greater detail into a memory.

        4. other: This has nothing to do with our wedding. Answer the query as normal.
        
        5. fact_summary: Generate a summary of facts about the wedding's information.  (e.g. close restaurants, close activities, venue information, cermony and reception times, etc.)
        
        6.  Memory: This is the memory data that needs to either be updated or the memory that is a duplicate. You Must return the full memory as a python list data structure that needs to be updated or is a duplicate.
        
        Use the existing memories to analysis whether the information is already in memory or not. If it is **similar** to an existing memory below then classify the request as 'duplicate'.
        Memories:\n {memories}
        '''
        response = self.client.responses.parse(
            model="gpt-4o",
            input=[{"role": "system", "content": sys_prompt}],
            tools=[{ "type": "web_search_preview" }],
            text_format=FactResponse,
            store=False,
            # stream=True
        )
        
        return response.output_parsed
if __name__ == "__main__":
    agent = WeddingAgent2()
    
    
    while True:
        query = input("User Query: ")
        
        with Session(engine) as session:
            conversation_history = get_conversation_messages(session,1)
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10]
        
        if query.lower() == "exit":
            print("Exiting Agent...")
            break
        
        memories = agent.get_memories(query=query)

        system_prompt = agent._system_prompt( memories=memories)
        
        # conversation_history.insert(0,{"role": "system", "content": system_prompt})
        # print(conversation_history)
        inputs = agent._generate_input(query=query, system_prompt=system_prompt)
        
        if len(conversation_history) != 0:
            for input_index in range(len(conversation_history)):
                
                _insert_input = {"role": conversation_history[input_index].role, "content": conversation_history[input_index].content}
                
                inputs.insert(input_index + 1, _insert_input)
        
        # for input in inputs:
        #     print(input, "\n")
        response = agent.generate_response(inputs=inputs)
        
        # with Session(engine) as session:
        #     add_message(session, 1, "user", query)
        #     add_message(session, 1, "assistant", response)
            
        
        summary = agent.llm_summary(response, memories=memories)
        # print("SUMMARY:")
        print(summary)
        # print(response, "\n")
        # break
        print("\n===========================================")
        if summary.category == "fact":
            stored_memory = agent.store_memory(summary.fact_summary)
            if stored_memory == "error":
                print("ERROR Storing memory.")
                break
            print("Stored Memeory: ",stored_memory)
            print("")
        elif summary.category == "update":
            print("NEED to update\n")
            print(summary.memory)
            print(type(summary.memory))
            print("\n")

        break
        # print(f"\n{response}\n")
        print(response, "\n")
        # print(summary)

