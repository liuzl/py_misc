# encoding: UTF-8
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

response = client.chat.completions.create(
    #model="gpt-3.5-turbo",
    model="gemini-pro",
    messages=[
        {
            "role": "user",
            "content": "Hello, How are you?"
        }
    ],
    max_tokens=300,
)
print(response.model_dump_json())
