import requests
import json
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


ak = os.getenv("BAIDU_API_KEY")
sk = os.getenv("BAIDU_SECRET_KEY")


import qianfan

chat_comp = qianfan.ChatCompletion(ak=ak, sk=sk)

# 调用默认模型，即 ERNIE-Bot-turbo
resp = chat_comp.do(model="ERNIE-Bot-4", messages=[{
    "role": "user",
    "content": "who r u?"
}])

#print(resp)
print(json.dumps(resp.body, ensure_ascii=False))
