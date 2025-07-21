
# from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
# from models import Conversation, Message
from memory import get_or_create_conversation, get_conversation_messages, add_message, updateConversatinSummary
from db import engine, get_session
# from pydantic import BaseModel
from schemas import ChatRequest, ChatResponse
import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# app = FastAPI()

user_id = "12345adsf"



session = get_session()

# convo = get_or_create_conversation(session, user_id)

# print(convo[0].id, convo[0].user_id, convo[0].created_at)
# for i in convo[1]:
#     print(i.id, i.role, i.content, i.timestamp)
# msg = add_message(session, conversation_id, "TESTER", "This is a test")

def chat(request: ChatRequest, session: Session = Depends(get_session)):
    # Load/create conversation
    conversation = get_or_create_conversation(session, request.user_id, request.id)
    convo = conversation[0]["conversation"]
    messages = conversation[0]["messages"]
    print("Messages:", messages)
    print("Convo:", convo)
    return

    # return convo
    history = [{"role": m.role, "content": m.content} for m in convo[1]]
    print(history)
    if history == []:
        system_message = {"role": "system", "content": "You are an expert assistant. You MUST return a summary of the chat history in a field called summary. Within your response you MUST return a JSON object of `{`summary: <summary of chat history>, text: <your response text>`}`. You MUST return a valid JSON string"}
        history.append(system_message)
    print(history)

    
    # Save user's message
    add_message(session, convo[0].id, "user", user_input)
    
    while True:
        user_input = input("Enter your message (or 'exit' to quit): ")
        if( user_input.lower() == 'exit'):
            print("Exiting chat.")
            return
        
        # print("User: ", user_input)
        history.append({"role": "user", "content": user_input})
        print("History: ", history)
        
        response = client.responses.create(
            model="gpt-4o",
            input=history,
            # previous_response_id=convo.last_response_id,
            store=False  # Set to True if you want OpenAI to retain conversation
        )

        reply = response.output[0].content[0].text
        res_dict = json.loads(reply)
        print(res_dict)
        updateSum = updateConversatinSummary(session, convo[0].id, res_dict['summary'])
        print(updateSum.summary)
        # print(res_dict['summary'])
        # print(res_dict['text'])

    return


    # Send to OpenAI Responses API
    response = client.responses.create(
        model="gpt-4o",
        input=request.message,
        # previous_response_id=convo.last_response_id,
        store=False  # Set to True if you want OpenAI to retain conversation
    )

    reply = response.output[0].content[0].text

    print("Reply from OpenAI:", reply)
    return

    # Save assistant reply
    add_message(session, convo.id, "assistant", reply)

    # Update response_id for conversation state
    convo.last_response_id = response.id
    session.add(convo)
    session.commit()

    return ChatResponse(response=reply)

# chatReq = ChatRequest(user_id=user_id, message="Hello, how are you?", id=3)
# chat(chatReq, session)

def testWebsearch():

    response = client.responses.create(
        model="gpt-4o",
        tools=[{ "type": "web_search_preview" }],
        input="Who won the 2025 PGA The Open?",
    )

    print(response.output[1].content[0].text)
    return
    res = {'id': 'resp_687d9b40789c819aa851784cdf6183440639036dc9a125aa', 'created_at': 1753062208.0, 'error': None, 'incomplete_details': None, 'instructions': None, 'metadata': {}, 'model': 'gpt-4o-2024-08-06', 'object': 'response', 'output': [{'id': 'ws_687d9b40d390819a993bc90dc4c27e8e0639036dc9a125aa', 'action': {'query': '2025 PGS US Open winner', 'type': 'search'}, 'status': 'completed', 'type': 'web_search_call'}, {'id': 'msg_687d9b42b1b8819abf696141cce016a60639036dc9a125aa', 'content': [{'annotations': [{'end_index': 435, 'start_index': 322, 'title': 'US Open 2025: JJ Spaun Holes Miracle 65-Foot Birdie Putt At The 72nd Hole To Win Maiden Major In The Rain At Oakmont', 'type': 'url_citation', 'url': 'https://www.golfmonthly.com/news/live/us-open-golf-2025-leaderboard-scores?utm_source=openai'}, {'end_index': 699, 'start_index': 487, 'title': 'US Open 2025: JJ Spaun Holes Miracle 65-Foot Birdie Putt At The 72nd Hole To Win Maiden Major In The Rain At Oakmont', 'type': 'url_citation', 'url': 'https://www.golfmonthly.com/news/live/us-open-golf-2025-leaderboard-scores?utm_source=openai'}, {'end_index': 854, 'start_index': 702, 'title': 'SDSU alum J.J. Spaun wins first major at 2025 U.S. Open', 'type': 'url_citation', 'url': 'https://www.axios.com/local/san-diego/2025/06/16/jj-spaun-wins-us-open-2025?utm_source=openai'}], 'text': "J.J. Spaun won the 2025 U.S. Open golf championship, held from June 12–15 at Oakmont Country Club in Pennsylvania. He secured his first major title with a final score of 1-under-par 279, finishing two strokes ahead of Robert MacIntyre. Spaun's victory was highlighted by a remarkable 64-foot birdie putt on the 18th hole. ([golfmonthly.com](https://www.golfmonthly.com/news/live/us-open-golf-2025-leaderboard-scores?utm_source=openai))\n\n\n## J.J. Spaun's Triumph at the 2025 U.S. Open:\n- [US Open 2025: JJ Spaun Holes Miracle 65-Foot Birdie Putt At The 72nd Hole To Win Maiden Major In The Rain At Oakmont](https://www.golfmonthly.com/news/live/us-open-golf-2025-leaderboard-scores?utm_source=openai)\n- [SDSU alum J.J. Spaun wins first major at 2025 U.S. Open](https://www.axios.com/local/san-diego/2025/06/16/jj-spaun-wins-us-open-2025?utm_source=openai) ", 'type': 'output_text', 'logprobs': []}], 'role': 'assistant', 'status': 'completed', 'type': 'message'}], 'parallel_tool_calls': True, 'temperature': 1.0, 'tool_choice': 'auto', 'tools': [{'type': 'web_search_preview', 'search_context_size': 'medium', 'user_location': {'type': 'approximate', 'city': None, 'country': 'US', 'region': None, 'timezone': None}}], 'top_p': 1.0, 'background': False, 'max_output_tokens': None, 'max_tool_calls': None, 'previous_response_id': None, 'prompt': None, 'reasoning': {'effort': None, 'generate_summary': None, 'summary': None}, 'service_tier': 'default', 'status': 'completed', 'text': {'format': {'type': 'text'}}, 'top_logprobs': 0, 'truncation': 'disabled', 'usage': {'input_tokens': 312, 'input_tokens_details': {'cached_tokens': 0}, 'output_tokens': 279, 'output_tokens_details': {'reasoning_tokens': 0}, 'total_tokens': 591}, 'user': None, 'prompt_cache_key': None, 'safety_identifier': None, 'store': True}
    
    print(res['output'][1]['content'][0]['annotations'])
    print(res['output'][1]['content'][0]['text'])
    
    print(len(res['output']))
    
    
testWebsearch()