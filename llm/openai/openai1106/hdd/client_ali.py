import requests
import json
from tqdm import tqdm

def run(i):
    url = f"https://milo-test.oss-cn-zhangjiakou.aliyuncs.com/hdd/batch1/image{i:03}.png"
    data = {"images":[{"image_url":url}]}
    response = requests.post("http://127.0.0.1:9001/hdd/item_recognition", data=json.dumps(data))
    return response

out = open("result.txt", "w")
for i in tqdm(range(1, 101)):
    response = run(i)
    out.write(f"{response.text}\n")
    print(response.text)
out.close()

#ret = run(1)
#print(ret)
