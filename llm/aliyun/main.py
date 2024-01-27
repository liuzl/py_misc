import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from http import HTTPStatus
import dashscope

model = 'qwen-vl-plus'
model = 'qwen-vl-max'

url = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"
url = 'https://milo-test.oss-cn-zhangjiakou.aliyuncs.com/hdd/batch1/image009.png'

prompt = "这是什么?"
prompt = open("prompt.md", "r").read()

def simple_multimodal_conversation_call():
    """Simple single round multimodal conversation call.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"image": url},
                {"text": prompt}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model=model, messages=messages)
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.


if __name__ == '__main__':
    simple_multimodal_conversation_call()
