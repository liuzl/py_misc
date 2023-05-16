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
