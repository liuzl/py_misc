from requests_html import HTMLSession
url = 'http://www.pbc.gov.cn/goutongjiaoliu/113456/113469/index.html'
session = HTMLSession()
r = session.get(url)
r.html.render(sleep=1, keep_page=True)
for node in r.html.find('font.newslist_style > a'):
    print(list(node.absolute_links)[0], node.text)
