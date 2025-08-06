from openai import OpenAI
from pydantic import BaseModel
import os
from typing import Literal
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class FactResponse(BaseModel):
    content: str
    date: str
    time: str
    response: str
    cateory: Literal["fact", "question", "other"]

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information and classify whether it into a category."},
        {
            "role": "user",
            "content": "tell me a story",
        },        
    ],
    text_format=FactResponse,
)

event = response.output_parsed

print(event)