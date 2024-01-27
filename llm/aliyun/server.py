from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import click
import os, re, json
import dashscope
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

PROMPT = open("prompt.md", "r").read()

#MODEL = 'qwen-vl-plus'
MODEL = 'qwen-vl-max'

class ResultDetail(BaseModel):
    category: str | None = None
    freshness: float | None = None
    quantity: int | None = None
    value: float | None = None
    recyclable: bool | None = None
    description: str | None = None

class ImageURL(BaseModel):
    image_url: str

class Request(BaseModel):
    category: str | None = None
    description: str | None = None
    system: str | None = None
    images: List[ImageURL] = []

def str_to_item(text):
    print("="*20)
    print(text)
    print("="*20)
    matched_content = re.search(r"```json\s([\s\S]+?)\s```", text)
    if matched_content:
        try:
            return ResultDetail(**json.loads(matched_content.group(1)))
        except Exception as e:
            print(e)
    try:
        return ResultDetail(**json.loads(text))
    except Exception as e:
        print(e)
    return ResultDetail(description=text)

def describe(image, prompt=PROMPT, model=MODEL):
    print(MODEL)
    messages = [{"role": "user","content": [{"image": image}, {"text": prompt}]}]
    response = dashscope.MultiModalConversation.call(model=model, messages=messages)
    print(response)
    return response


app = FastAPI()

@app.post("/hdd/item_recognition")
def item_recognition(item: Request) -> ResultDetail:
    if len(item.images) == 0:
        raise HTTPException(status_code=400, detail="images is empty")
    try:
        response = describe(item.images[0].image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=response.message)
        item = str_to_item(response.output.choices[0].message.content[0]['text'])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    return item

@click.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=9001)
@click.option("--model", default=MODEL)
def main(host: str, port: int, model: str):
    global MODEL
    MODEL = model
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
