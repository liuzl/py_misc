# encoding: UTF-8
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("API_BASE")
openai.api_key = os.getenv("API_KEY")

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages = messages,
        temperature = 0,
    )
    return response.choices[0].message["content"]


def test():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages = [{"role":"user","content":"Write en poem about Summer in Chinese"},],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(response)

#test()
prompt = 'Write en poem about Summer in Chinese, 李白的风格'
print(get_completion(prompt))
