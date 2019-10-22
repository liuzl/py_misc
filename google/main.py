import requests
import lxml
import lxml.html

url_ = 'https://www.google.com/search?q=%22Zhongguancun%22+%22Forum%22+%222019%22&tbm=nws&start='

def extract(page):
    doc = lxml.html.document_fromstring(page)
    rec = doc.xpath("//div[@class='g']")
    print(len(rec))
    for idoc in rec:
        title = idoc.xpath(".//h3")
        link = idoc.xpath(".//h3//a/@href")
        snippet = idoc.xpath(".//div[@class='st']")
        time = idoc.xpath(".//div[@class='slp']/span[3]")
        print(title,link,snippet,time)

url = url_ + "10"
res = requests.get(url)
extract(res.text)
