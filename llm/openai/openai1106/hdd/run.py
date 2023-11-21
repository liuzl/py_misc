import pandas as pd
import openpyxl
import openpyxl.drawing.image
import base64
import json
import os
import openai
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

gpt_prompt='''任务简介：
- 识别图片中的主要物品，判断其分类并评估新旧程度。

分类标准：
- 服装：大衣、皮衣、半袖、裤子、裙子、内衣裤、秋衣类、毛衣类、工装、校服。
- 家电：空气净化器、厨房家电、家居家电。
- 乐器：电子乐器、琴类。
- 玩具：小件（手办）、大件、毛绒玩具。
- 图书：儿童绘本、课外书、小说、套装书籍、课本。
- 手机：智能手机、功能机。
- 笔记本电脑：品牌电脑、非品牌电脑。

回答格式（JSON）：
{
    "exist": "是/否",
    "category": {
        "primary": "一级分类",
        "secondary": "二级分类"
    },
    "freshness": "新/旧/中等"
}
'''

def extract_images_from_xlsx(file_path):
    workbook = openpyxl.load_workbook(filename=file_path)
    images = []

    for sheet in workbook.worksheets:
        for drawing in sheet._images:
            if isinstance(drawing, openpyxl.drawing.image.Image):
                images.append(drawing)

    return images

def read_xls_with_images(file_path):
    df = pd.read_excel(file_path, keep_default_na=False)
    images = extract_images_from_xlsx(file_path)
    assert len(df) == len(images)
    df["image"] = images
    return df

def describe(b64image, prompt=gpt_prompt):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": b64image,
                        "detail": "low",
                    }
                }
            ]
        }],
        max_tokens=300,
    )
    print(response.model_dump_json())
    return response

def process(image: openpyxl.drawing.image.Image):
    x = f"data:image/{image.format};base64,{base64.b64encode(image.ref.getvalue()).decode()}"
    response = describe(x)
    s = response.choices[0].message.content.lstrip("```json\n").rstrip("\n```")
    item = json.loads(s)
    exist = item["exist"]
    primary = secondary = freshness = ""
    if exist == "是":
        primary = item["category"]["primary"]
        secondary = item["category"]["secondary"]
        freshness = item["freshness"]
    return exist, primary, secondary, freshness, response.usage.total_tokens, json.dumps(item, ensure_ascii=False), response.model_dump_json()

def main():
    ifile = "data.xlsx"
    ofile = "data2.xlsx"
    df = read_xls_with_images(ifile)
    
    #df = df.head(5)
    
    df["exist"], df["primary"], df["secondary"], df["freshness"], df["tokens"], df["json"], df["model_output"] = zip(*df["image"].map(process))

    df.drop('image', axis=1).to_excel(ofile, index=False)
    
    workbook = openpyxl.load_workbook(ofile)
    sheet = workbook.active

    sheet.column_dimensions['E'].width = 20

    for i in range(2, len(df) + 2):
        sheet.row_dimensions[i].height = 160

    for index, row in df.iterrows():
        image = row['image']
        image.width = 160
        image.height = 200
        cell = 'E' + str(index + 2)
        sheet.add_image(image, cell)

    workbook.save(ofile)

if __name__ == "__main__":
    main()