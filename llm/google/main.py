import google.generativeai as palm
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

palm.configure(api_key=os.getenv('API_KEY'))
response = palm.generate_text(prompt="The opposite of hot is")
print(response.result) #  'cold.'
