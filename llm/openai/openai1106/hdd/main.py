import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

gpt_prompt1='''任务简介：
- 识别每张图片中的主要物品，判断其分类并评估新旧程度。

分类标准：
- 服装：大衣、皮衣、半袖、裤子、裙子、内衣裤、秋衣类、毛衣类、工装、校服。
- 家电：空气净化器、厨房家电、家居家电。
- 乐器：电子乐器、琴类。
- 玩具：小件（手办）、大件、毛绒玩具。
- 图书：儿童绘本、课外书、小说、套装书籍、课本。
- 手机：智能手机、功能机。
- 笔记本电脑：品牌电脑、非品牌电脑。

对于没有给出分类的物品，可以自行判断分类，此时exist设置为"否"。

回答格式（JSON）：
[{
    "exist": "是/否",
    "category": {
        "primary": "一级分类",
        "secondary": "二级分类"
    },
    "freshness": "新/旧/中等"
}]
'''

def describe_multiple(images, prompt=gpt_prompt1):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [{"type": "text", "text": prompt},] + 
            [{"type": "image_url", "image_url": {"url": image, "detail": "low",}} for image in images]
        }],
        max_tokens=3000,
    )
    print(response.model_dump_json())
    return response

def main():
    urls = [f"https://milo-test.oss-cn-zhangjiakou.aliyuncs.com/hdd/batch1/image{i+1:03}.png" for i in range(241)]
    images_array =[urls[:100], urls[100:200], urls[200:]]
    with open("out.jsonl", "w") as out:
        for images in images_array:
            print(images)
            print([{"type": "image_url", "image_url": {"url": image, "detail": "low",}} for image in images])
            #response = describe_multiple(images)
            #out.write(response.model_dump_json() + "\n")
            #out.flush()

if __name__ == "__main__":
    main()