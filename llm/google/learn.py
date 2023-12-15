import os
import json
import requests
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


'''
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$API_KEY \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[{
          "text": "Write a story about a magic backpack."}]}]}' 2> /dev/null
'''

model = "gemini-pro"
prompt = "北京下大雪了，以李白的风格写一首诗：\n"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={os.getenv('GOOGLE_API_KEY')}"
headers = {"Content-Type": "application/json"}
data = {
    "contents": [{
        "parts":[{
            "text": prompt
        }]
    }]
}
ret = requests.post(url, json.dumps(data), headers=headers)
print(ret.json())

'''
{'candidates': [{'content': {'parts': [{'text': '北风卷地雪纷纷，\n白雪飘零盖乾坤。\n长安城中万籁俱寂，\n唯有雪落的声音。\n\n李白独自站在高楼之上，\n看着漫天飞舞的雪花，\n思绪万千。\n\n他想起家乡的雪，\n那也是这样的大雪纷飞，\n可是家乡的雪是温暖的，\n因为它
有家乡人的陪伴。\n\n长安的雪是寒冷的，\n因为它没有家乡人的陪伴。\n李白感到非常的孤单和寂寞。\n\n他拿起酒杯，\n饮下了一杯酒，\n希望能借酒消愁。\n\n可是，酒并不能让他忘记自己的乡愁。\n他只觉得更加的孤独和寂寞。\n\n于是，他决定离开长安，\n去寻找自己的家乡。\n\n他在雪地里跋涉了很久，\n终于回到了自己的家乡。\n\n看到家乡的亲人，\n李白感到非常的温暖和幸福。\n\n他知道，自己终于找到了自己的家。'}], 'role': 'model'}, 'finishReason': 'STOP', 'index': 0, 'safetyRatings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE'}]}], 'promptFeedback': {'safetyRatings': [{'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HATE_SPEECH', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_HARASSMENT', 'probability': 'NEGLIGIBLE'}, {'category': 'HARM_CATEGORY_DANGEROUS_CONTENT', 'probability': 'NEGLIGIBLE'}]}}
'''