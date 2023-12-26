from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import click
import os, re, json
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)

PROMPT = '''识别图片中的一个主要物品，判断其分类并评估新旧程度。

分类标准：
```python
categories = {
    "服装": ["大衣", "皮衣", "半袖", "裤子", "裙子", "内衣裤", "秋衣类", "毛衣类", "工装", "校服", "鞋子", "拖鞋"],
    "家电": ["空气净化器", "厨房家电", "家居家电", "其它"],
    "乐器": ["电子乐器", "琴类", "其它"],
    "玩具": ["小件（手办）", "大件", "毛绒玩具"],
    "图书": ["儿童绘本", "课外书", "小说", "套装书籍", "课本"],
    "手机": ["智能手机", "功能机"],
    "笔记本电脑": ["品牌电脑", "非品牌电脑"]
}
```

对于没有给出分类的物品，可以自行判断分类，但此时exist的值必须设置为"否"。

回答格式（JSON），一级分类和二级分类必须与categories中定义的一致：
```json
{
    "exist": "是/否",
    "category": {
        "primary": "一级分类",
        "secondary": "二级分类"
    },
    "freshness": "新/旧/中等",
    "quantity": NUMBER,
    "description": "描述"
}
```
'''

#MODEL = "gpt-4-vision-preview"
MODEL = "gemini-pro-vision"

class Category(BaseModel):
    primary: str
    secondary: str

class ResultDetail(BaseModel):
    exist: str
    category: Category | None = None
    freshness: str | None = None
    quantity: int | None = None
    description: str | None = None

def str_to_item(text):
    matched_content = re.search(r"```json\s([\s\S]+?)\s```", text)
    if matched_content:
        try:
            return ResultDetail(**json.loads(matched_content.group(1)))
        except:
            pass
    return ResultDetail(description=text)

def describe_multiple(images, prompt=PROMPT, model=MODEL):
    print(MODEL)
    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [{"type": "text", "text": prompt},] + 
            [{"type": "image_url", "image_url": {"url": image, "detail": "low",}} for image in images]
        }],
        max_tokens=256,
        temperature=0.0,
    )
    #print(response.model_dump_json())
    return response

app = FastAPI()


@app.get("/result")
def get_result(url: str) -> ResultDetail:
    url = url.strip()
    if url == "":
        raise HTTPException(status_code=400, detail="url is empty")
    try:
        response = describe_multiple([url])
        item = str_to_item(response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return item

@click.command()
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=9000)
@click.option("--model", default=MODEL)
def main(host: str, port: int, model: str):
    global MODEL
    MODEL = model
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    main()
