# encoding: UTF-8
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = ""

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model = os.getenv("MODEL"),
        max_tokens = 1024,
        messages = messages,
        temperature = 0,
    )
    return response.choices[0].message["content"]


prompt = f"""
Translate the following English text to Chinese: \
```Hi, I would like to order a blender```
"""
print(get_completion(prompt))
