import urllib.parse
from requests_html import HTMLSession
url = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html'
data = []
while True:
    print(url)
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True)
    for node in r.html.find('font.newslist_style > a'):
        data.append({'url':list(node.absolute_links)[0], 'title':node.text})
    link = r.html.find("a:contains('下一页')")
    if len(link) <= 0:
        break
    url = urllib.parse.urljoin(link[0].base_url, link[0].attrs['tagname'])
    session.close()
import pandas as pd
df = pd.DataFrame(data)
df.to_csv("pbc_news.csv", index=None)
