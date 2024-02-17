# encoding=UTF-8
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_API_BASE"),
    api_key = os.getenv("OPENAI_API_KEY"),
)

fname = "D:\\git\\py_misc\\deepfilternet\\zjx1.mp3"

result = client.audio.transcriptions.create(
    model="whisper-1",
    file=open(fname, "rb"),
    prompt="这是一段医学领域的语音，胸片有正位和侧位的。请注意需要有准确的中文标点符号。",
    response_format="verbose_json",
    timestamp_granularities=["word"],
)
print(result)
