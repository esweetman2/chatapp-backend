from openai import OpenAI
# from pydantic import BaseModel, Field
import os
# from typing import Literal, List
from dotenv import load_dotenv
# from Backend.db import engine, Session
# from Backend.Agents.WeddingAgent.WeddingMemory import MemoryMangement
# from memory import add_message, get_conversation_messages
from Backend.Agents.Tools.Tools import tools
from Backend.Agents.Tools.GoogleSheets import GoogleSheets
import json
load_dotenv()


# class FactResponse(BaseModel):
#     fact_summary: str
#     response: str
#     category: Literal["fact","duplicate", "update", "other"]
#     memory: List[str] = Field(..., description="A list of relevant memories or pieces of information associated with the fact including the memory id.")
#     reason: str
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


  
class Agent:
    def __init__(self, model):
        self.openai_key = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        
        
    def generate_response(self, inputs):
        try:
            response = client.responses.create(
                model=self.model,
                input=inputs,
                tools=tools,
                # text_format=FactResponse,
                stream=True,
                store=False,
            )
            events = []

            for event in response:
                events.append(event)
            
            return events
            return response
            
        except Exception as e:
            print(e)
            return None
        
        # return "Testing"

        # llm_response = response.output
        # return response

    # def stream(self):
    #     stream = client.responses.create(
    #         model="gpt-5",
    #         input=[
    #             {
    #                 "role": "user",
    #                 "content": "Tell me a short story about a programmer and coffee.",
    #             },
    #         ],
    #         stream=True,
    #         store=False
    #     )

    #     for event in stream:
    #         if event.type == "response.output_text.delta":
    #             print(event.delta, end="", flush=True)

def googleSheet_test():
    _agent = Agent("gpt-4o")
    inputs = [{
                "role": "system",
                "content": "You're a helpful assistant"
            },
            {
              "role": "user",
              "content": "What is the schedule for the honeymoon trip?"    
              
              }]
    res = _agent.generate_response(inputs=inputs)

    if res is None:
        print("res is None")
        return


#### Streaming logic. #########
    final_tool_calls = {}
    final_tool_output = None
    for event in res:
        print(event.type)
        if event.type == 'response.output_item.added':
            final_tool_calls[event.output_index] = event.item
        elif event.type == 'response.function_call_arguments.delta':
            index = event.output_index

            if final_tool_calls[index]:
                final_tool_calls[index].arguments += event.delta
        # elif event.type == 'response.function_call_arguments.done':
        #     final_tool_output.append(event)
        elif event.type == 'response.output_item.done':
            print()
            # final_tool_output = event
            # return
        elif event.type == "response.completed":
            # print(event)
            final_tool_output = event.response.output

    # return
    # print(final_tool_calls)
    print("\n")
    print(final_tool_output)
    print("\n")
    function_input =[]


    for i in final_tool_output:
        obj = {
            "arguments": i.arguments,
            "call_id": i.call_id,
            "name": i.name,
            "type": i.type,
            "id": i.id,
            "status": i.status
        }

        function_input.append(obj)

        # print(i.name)



    # print(type(final_tool_output))
    # return

    # print(final_tool_calls)
    # print(final_tool_calls[0].call_id)

    # return
    inputs += function_input

    arguments = json.loads(final_tool_calls[0].arguments)


    _GoogleSheets = GoogleSheets()
    # print(function_call_arguments)
    result = {"read_google_sheet": _GoogleSheets.read_google_sheet(arguments["google_sheet_name"], arguments["worksheet"])}
    # print("Function call result: ", result)
    # 4. Provide function call results to the model
    # inputs.append({
    #     "role": "assistant",
    #     "content": [{
    #         "type": "tool_result",
    #         "tool_name": final_tool_calls[0].name,
    #         "output_text": json.dumps(result)
    #         }]
    # })
    inputs.append({
        "type": "function_call_output",
        "call_id": final_tool_calls[0].call_id,
        "output": json.dumps(result),
    })
    
    # # print(inputs)

    # # return

    ####### NON STREMAING LOGIC #####
    # Save function call outputs for subsequent requests
    # function_call = None
    # function_call_arguments = None
    # inputs += res.output
    # for item in res.output:
    #     if item.type == "function_call":
    #         function_call = item
    #         function_call_arguments = json.loads(item.arguments)

    # # 3. Execute the function logic for get_horoscope
    # _GoogleSheets = GoogleSheets()
    # print(function_call_arguments)
    # result = {"read_google_sheet": _GoogleSheets.read_google_sheet(function_call_arguments["google_sheet_name"], function_call_arguments["worksheet"])}
    # # print("Function call result: ", result)
    # # 4. Provide function call results to the model
    # inputs.append({
    #     "type": "function_call_output",
    #     "call_id": function_call.call_id,
    #     "output": json.dumps(result),
    # })

    # print("Final input:")
    # print(inputs)
    # return

    response = client.responses.create(
        model="gpt-4o",
        instructions="Respond only with a horoscope generated by a tool.",
        tools=tools,
        input=inputs,
        stream=True
    )
    
    for event in response:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)


    # # 5. The model should be able to give a response!
    # print("Final output:")
    # print(response.model_dump_json(indent=2))
    # print("\n" + response.output_text)

def token_test():
    import tiktoken

    # Choose the encoding based on the model
    encoding = tiktoken.encoding_for_model("gpt-4")

    # Sample text
    text = "Hello, how are you doing today?"

    # Encode the text to get token IDs
    token_ids = encoding.encode(text)

    print("Token IDs:", token_ids)
    print("Number of tokens:", len(token_ids))  


if __name__ == '__main__':
    # _agent = Agent("gpt-4o")

    # _agent.stream()

    googleSheet_test()

    
    # test = _agent.generate_response([{
    #             "role": "system",
    #             "content": "You're a helpful assistant"
    #         },
    #         {
    #           "role": "user",
    #           "content": "This is a test request"    
              
    #           }])
    # print(test)

    


