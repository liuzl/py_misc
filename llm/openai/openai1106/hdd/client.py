import requests
import json
import base64

url = "https://milo-test.oss-cn-zhangjiakou.aliyuncs.com/hdd/batch1/image071.png"
image = base64.b64encode(requests.get(url).content).decode("utf-8")
data = {"images":[{"image_b64":f"data:image/png;base64,{image}"}]}
response = requests.post("http://192.168.1.32:9001/hdd/item_recognition", data=json.dumps(data))
print(response.text)
