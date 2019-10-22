import requests
import json
from collections import defaultdict
import re
from tqdm import tqdm
import langid

lines = open('google1.json').read().strip().split('\n')

def ner(text):
    query = json.dumps({'doc':text})
    res = requests.post('http://36.112.85.6:4501/nlp/en/ner_dl',query).json()
    d = defaultdict(list)
    for item in res:
        for ent in item['entities']:
            d[ent['type']].append(ent['text'])
    return d

def domain(url):
    x = re.findall(r'://(.+?)/', url)
    if len(x) > 0: return x[0]
    return ''

def lang(text):
    return langid.classify(text)[0]

out = open("zgc_google.txt", "w")
for line in tqdm(lines):
    #print(line)
    item = json.loads(line)
    item['domain'] = domain(item['url'])
    item['title_ent'] = ner(item['title'])
    item['snippet_ent'] = ner(item['snippet'])
    item['lang'] = lang(item['title'] + " " + item['snippet'])
    out.write(json.dumps(item)+"\n")
    out.flush()
out.close()

