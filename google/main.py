import requests
import lxml
import lxml.html
import datetime
import json
from tqdm import tqdm

common_headers = {
'Connection': 'keep-alive',
'Accept': '*/*',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
'Referer': 'http://m.zhugefang.com/spa/view/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
}

url_ = 'https://www.google.com/search?q=%22Zhongguancun%22+%22Forum%22+%222019%22&tbm=nws&start='

def extract(page):
    now = datetime.datetime.now()
    doc = lxml.html.document_fromstring(page)
    rec = doc.xpath("//div[@class='g']")
    for idoc in rec:
        title = idoc.xpath(".//h3")
        if len(title) > 0: title = lxml.etree.tounicode(title[0], method='text')
        else: title = ""
        link = idoc.xpath(".//h3//a/@href")
        if len(link) > 0: link = link[0]
        else: link = ""
        snippet = idoc.xpath(".//div[@class='st']")
        if len(snippet) > 0: snippet = lxml.etree.tounicode(snippet[0], method='text')
        else: snippet = ""
        time = idoc.xpath(".//div[@class='slp']/span[3]")
        if len(time) > 0: time = lxml.etree.tounicode(time[0], method='text')
        else: time = ""
        item = {"title": title, "url": link, "snippet": snippet, "time": time, "now":str(now)}
        yield item

out = open("google1.json", "a")
t = tqdm(total=187)
for i in range(187):
    t.update(1)
    url = url_ + "%d"%i
    res = requests.get(url, headers=common_headers)
    for item in extract(res.text):
        line = json.dumps(item, ensure_ascii=False)
        out.write(line+"\n")
        out.flush()
out.close()

