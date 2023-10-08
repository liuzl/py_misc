from litellm import completion
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

messages = [{ "content": "Hello, how are you?","role": "user"}]
response = completion(model="gpt-3.5-turbo", messages=messages)

print(response.choices[0].message["content"])
