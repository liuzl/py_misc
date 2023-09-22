# encoding: UTF-8
#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_type = "azure"
openai.api_base = os.getenv("API_BASE")
openai.api_version = os.getenv("API_VERSION")
openai.api_key = os.getenv("API_KEY")

def get_completion(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine = os.getenv("ENGINE"),
        messages = messages,
        temperature = 0,
    )
    return response.choices[0].message["content"]


def test():
    response = openai.ChatCompletion.create(
        engine=os.getenv("ENGINE"),
        messages = [{"role":"user","content":"Write en poem about Summer"},],
        temperature=0.5,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    print(response)

text = f"""
You should express what you want a model to do by \
providing instructions that are as clear and \
specific as you can possibly make them. \
This will guide the model towards the desired output, \
and reduce the chances of receiving irrelevant \
or incorrect responses. Don't confuse writing a \
clear prompt with writing a short prompt. \
In many cases, longer prompts provide more clarity \
and context for the model, which can lead to \
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \
into a single sentence. The response should be in Chinese.
```{text}```
"""
response = get_completion(prompt)
print(response)
