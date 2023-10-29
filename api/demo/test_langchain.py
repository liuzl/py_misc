import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.prompts import PromptTemplate

PHONE_CALL_TEMPLATE = """
The following is a friendly conversation between a human and an AI. 
The AI's name is Ling. 她需要收集大家下周秋游是否能去，以及合适的具体时间。

她的目的是收集大家的意见，以便安排秋游的时间。收集到信息之后需要再次确认一下。
请尽量简短回答，不要超过一句话。不要问秋游之外的任何其他问题。

Current conversation:
{history}
Human: {input}
AI:"""

PHONE_CALL_PROMPT = PromptTemplate(
    input_variables=["history", "input"], template=PHONE_CALL_TEMPLATE
)

llm = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2048)
conversation = ConversationChain(
    llm=llm, 
    prompt=PHONE_CALL_PROMPT,
    memory = memory,
    verbose = True
)

while True:
    input_text = input("Human:")
    if input_text == "exit":
        break
    output_text = conversation.predict(input=input_text)
    print("AI:", output_text)