# encoding: UTF-8
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url=os.getenv("BASE_URL"),
)

response = client.chat.completions.create(
    model="moonshot-v1-8k",
    messages=[
        {
            "role": "user",
            "content": "Hello, How are you?"
        }
    ],
    max_tokens=300,
)
print(response.model_dump_json())
