# encoding: UTF-8
import os
import openai
import sys

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages = messages,
        temperature = 0,
    )
    return response.choices[0].message["content"]



#test()
if len(sys.argv) > 1:
    model = sys.argv[1]
else:
    model = "gpt-3.5-turbo"

if len(sys.argv) > 2:
    prompt = sys.argv[2]
else:
    prompt = 'Which city is the capital of Japan?'
print(get_completion(prompt=prompt, model=model))
