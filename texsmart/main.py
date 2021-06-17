# -*- coding: utf8 -*-
import json
import requests

obj = {"str": "他在看流浪地球。"}
req_str = json.dumps(obj).encode()

url = "https://texsmart.qq.com/api"
r = requests.post(url, data=req_str)
r.encoding = "utf-8"
print(r.text)
#print(json.loads(r.text))
