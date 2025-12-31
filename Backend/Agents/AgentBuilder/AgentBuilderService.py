'''

This is class for constructing agents to do functionality.


'''


import tiktoken
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
from Backend.Database.ChatsDatabase import ChatsDatabase
from Backend.Database.MessagesDatabase import MessagesDatabase
from Backend.Database.MemoryDatabase import MemoryDatabase
from Backend.Database.AgentToolsDatabase import AgentToolsDatabase
from Backend.Database.LLMModelDatabase import LLMModelDatabase
from Backend.Database.ChatsDatabase import ChatsDatabase
from Backend.Agents.Tools.GoogleSheets import GoogleSheets
# from Backend.Agents.ContextWindow.ContextWindowChecker import ContextWindowChecker
from Backend.Agents.Memory.base import MemoryFactory
from Backend.Agents.Tools.base import ToolFactory
from Backend.Agents.LLMInputs.base import LLMInputsFactory
from Backend.Agents.ContextWindow.base import ContextWindowFactory
from Backend.Agents.Summary.base import SummaryFactory
load_dotenv()

class AgentBuilderService:
    def __init__(self, db_session, agent_id: int, chat_id: int, query: str = "", role: str = "user", user_id: int = None):
        self.db_session = db_session
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._AgentDatabase = AgentDatabase(db_session)
        self.agent = self._AgentDatabase.get_agent(agent_id)
        self.chat_id = chat_id
        self.role = role
        self.query = query
        self.user_id = user_id
        self._MessagesDatabase = MessagesDatabase(self.db_session)
        self.messages = self._MessagesDatabase.get_message(chat_id=chat_id)
        self._ChatsDatabase = ChatsDatabase(self.db_session)

        self._MemoryDatabase = MemoryDatabase(self.db_session)
        self._AgentToolsDatabase = AgentToolsDatabase(self.db_session)
        self._LLMModelDatabase = LLMModelDatabase(self.db_session)
        self._GoogleSheets = GoogleSheets()

        if not self.agent:
            raise ValueError(f"Agent with id={agent_id} not found")
         
        self.chat_summary = self._ChatsDatabase.get_chat(id=chat_id)
        self.message_start_index = self.chat_summary.message_start_index
        self.agent_id = agent_id
        self.agent_name = self.agent.agent_name
        self.description = self.agent.description
        self.system_message = self.agent.system_message
        self.agent_model = self.agent.model
        self.use_memory = self.agent.use_memory
        self.agent_model_id = self.agent.model_id
        self.memory_table = "agentmemory"

        self.memory_factory = MemoryFactory.create_memory_strategy(self, agent_id=self.agent_id, use_memory=self.use_memory, memory_db=self._MemoryDatabase)
        self._ToolFactory = ToolFactory(db=self._AgentToolsDatabase, agent_id=self.agent_id)
        self.tools = self._ToolFactory.create_agent_tools()
        self.llm_input_factory = LLMInputsFactory(db=self._MessagesDatabase)
        self.context_window_factory = ContextWindowFactory(db=self._LLMModelDatabase)
        self.summary_factory = SummaryFactory(db=self._AgentDatabase)
    
    
    # def _get_message_history(self):
    #     messages = self._MessagesDatabase.get_message(chat_id=self.chat_id)
    #     if messages:
    #         message_list = []
    #         for message in messages:
    #             message_list.append({
    #                 "role": message.role,
    #                 "content": message.message
    #             })
    #         return message_list
    #     return []
    
    def _store_message(self, role: str, content: str):
        # _MessageDatabase = MessagesDatabase(self.db_session)
        # print(self.agent_id, self.user_id,self.chat_id, role, content)
        add_message = self._MessagesDatabase.add_message(
            user_id=self.user_id,
            agent_id=self.agent_id,
            chat_id=self.chat_id,
            message=content,
            role=role
        )
        # print(add_message)
        return add_message
    
    def _agent_setup(self):
        try:
            
            self._rolling_window_messages()
            
            memories = self.memory_factory.get_memories(query=self.query, memory_table=self.memory_table, top_k=10)
            self.system_message = self.system_message + f"\nYou MUST use the context below to help give a more accurate response.\n{str(memories)}"
            
            inputs = self.llm_input_factory.create_inputs_strategy(messages=self.messages, system_message=self.system_message, query=self.query, role=self.role)
            
            inputs.insert(0, {"role": "system", "content": self.system_message})

            # print(self.agent)
            
            context_check = self.context_window_factory.context_window_checker(
                agent_model=self.agent_model, 
                model_id=self.agent_model_id, 
                messages=inputs
                )

            agent = {
                "memories": memories,
                "context_check": context_check, 
                "inputs": inputs,
                "tools": self.tools,
                "system_message": self.system_message,
                "query": self.query,
            }
            
            return agent
        except Exception as e:
            print("Error storing agent response: ", str(e))
            agent_response = None
        
            return agent_response

    # def agent_orchestrator(self, agent_setup, summary, inputs):
    #     agent_setup["context_check"] = True
    #     print(agent_setup["context_check"])
    #     if agent_setup["context_check"] == True:
    #         # print("summarize")
    #         summary_agent = self.summary_factory.get_summary_agent()

    #         prepared_summary_agent = self.summary_factory.prepare_summary_agent(agent=summary_agent, summary=summary)

    #         summary_inputs = self.llm_input_factory.create_summary_inputs(inputs=inputs, index=self.message_start_index)

    #         prepared_summary_agent["new_index"] = summary_inputs["new_index"]
    #         prepared_summary_agent["inputs"] = summary_inputs["summary_messages"]
    #         prepared_summary_agent["memories"] = []

    #         # print(self.messages.index(prepared_summary_agent["inputs"][1]))
    #         self.handle_update_chat_index(self.messages,prepared_summary_agent["inputs"])
            
    #         return prepared_summary_agent
        
    #     else:
    #         return agent_setup
    # def handle_update_chat_index(self):
    #     new_index = len(self.messages) - 
    #     print(new_index)
        
    # def handle_summary_call(self, agent):

    #     response = self.client.responses.parse(
    #             model=agent["model"],
    #             input=agent["inputs"],
    #             # tools=[{ "type": "web_search_preview" }],
    #             tools=[],
    #             store=False,
    #         )
        
    #     return response.output_text
    
    def _rolling_window_messages(self):
        if self.messages and len(self.messages) > 10:
            self.messages = self.messages[-10:]
            return

    def generate_response(self):
        
        try:
            agent = self._agent_setup()

            response = self.client.responses.create(
                model=self.agent_model,
                input=agent["inputs"],
                # tools=[{ "type": "web_search_preview" }],
                tools=self.tools,
                store=False,
            )

            response_tools = self._ToolFactory.llm_response_tool_selector(response.output)
            
            if not response_tools:
                self._store_message(role=self.role, content=self.query)
                agent_response = self._store_message(role="assistant", content=response.output_text)
                # print("Agent Rsponse: ", agent_response)
                return agent_response
         
            function_call_inputs = self._ToolFactory.llm_response_tools(response_tools, self._GoogleSheets)

            second_inputs = agent["inputs"] + response.output + function_call_inputs
 
            function_call_response = self.client.responses.parse(
                model=self.agent_model,
                input=second_inputs,
                # stream=True,
                tools=self.tools,
                store=False,
            )
            

            self._store_message(role=self.role, content=self.query)
            agent_response = self._store_message(role="assistant", content=function_call_response.output_text)

            return agent_response
        except Exception as e:
            print("Error storing agent response: ", str(e))
            agent_response = None
            # return "Failed response"
        
            return agent_response
        
    def generate_response_stream(self):
        
        try:
            agent = self._agent_setup()

            # print(agent)
            agent_response = ""
            count = 0

            while True:
                # print("Running Count: ", count)
                if count == 5:
                    raise RuntimeError("Exceeded max tool calls")
                with  self.client.responses.create(
                    model=self.agent_model,
                    input=agent["inputs"],
                    # tools=[{ "type": "web_search_preview" }],
                    stream=True,
                    tools=self.tools,
                    store=False,
                ) as response:


                    final_tool_calls = {}
                    final_tool_output = None
                    for event in response:
                        # print(event.type)
                        if event.type == 'response.output_item.added':
                            final_tool_calls[event.output_index] = event.item
                        elif event.type == 'response.function_call_arguments.delta':
                            index = event.output_index
                            if final_tool_calls[index]:
                                final_tool_calls[index].arguments += event.delta
                        elif event.type == "response.completed":
                            final_tool_output = event.response.output
                        elif event.type == "response.output_text.delta":
                            agent_response += event.delta
                            yield event.delta
                


                    response_tools = self._ToolFactory.llm_response_tool_selector(final_tool_output)
                    # print("response_tools", response_tools)
                # return "testing"

                    if not response_tools:
                        break
                        # print("HRERE 2")

                        # self._store_message(role=self.role, content=self.query)
                        # agent_response = self._store_message(role="assistant", content=agent_response)
                    # print("Agent Rsponse: ", agent_response)
                    # return agent_response
                    # return
                # else:
                    function_call_inputs = self._ToolFactory.llm_response_tools(response_tools)

                    agent["inputs"] = agent["inputs"] + final_tool_output + function_call_inputs
        
                    # function_call_response = self.client.responses.create(
                    #     model=self.agent_model,
                    #     input=second_inputs,
                    #     stream=True,
                    #     tools=self.tools,
                    #     store=False,
                    # )

                    # for event in function_call_response:
                    #     # print(event.type)
                    #     if event.type == "response.output_text.delta":
                    #         agent_response += event.delta
                    #         yield event.delta
                count += 1    
                    
            # print("HRERE 1")
            self._store_message(role=self.role, content=self.query)
            # print("here: \n", agent_response)
            agent_response = self._store_message(role="assistant", content=agent_response)

                # return agent_response
        except Exception as e:
            print("Error storing agent response: ", str(e))
            agent_response = None
            # return "Failed response"
        
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


