#coding=utf-8
import re
import hashlib
try:
    import htmlentitydefs
except:
    import html.entities as htmlentitydefs

RE_IGNORE_BLOCK = {
'doctype' : r'(?is)<!DOCTYPE.*?>', # html doctype
'comment' : r'(?is)<!--.*?-->', # html comment
'script' : r'(?is)<script.*?>.*?</script>', # javascript
'style' : r'(?is)<style.*?>.*?</style>', # css
#'special' : r'&.{2,5};|&#.{2,5};',
}

RE_NEWLINE_BLOCK = {
'div' : r'(?is)<div.*?>',
'p' : r'(?is)<p.*?>',
'br' : r'(?is)<br.*?>',
'hr' : r'(?is)<hr.*?>',
'h' : r'(?is)<h\d+.*?>',
'li' : r'(?is)<li\d+.*?>',
}

RE_IMG = r'(?is)(<img.*?>)'
RE_A = r'(?is)(<a.*?>.+?</a>)'

RE_TAG = r'(?is)<.*?>'

ENCODINGS = ['gb18030', 'utf-8']

##
# http://effbot.org/zone/re-sub.htm#unescape-html
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def get_unicode_str(html):
    if isinstance(html, (unicode,)):
        return 'unicode', html
    elif isinstance(html, (str, )):
        for enc in ENCODINGS:
            try:
                html = html.decode(enc)
                return enc, html
            except:
                pass
    return '', html

def clean(html):
    encoding, html = get_unicode_str(html)
    if encoding == '': return ''
    html = '\n'.join([x.strip() for x in html.split("\n")])
    html = re.sub(r"(?is)</a><a",'</a> <a',html)
    html = re.sub(r"\n", '', html)
    for k,v in RE_IGNORE_BLOCK.iteritems():
        html = re.sub(v, '', html)
    for k,v in RE_NEWLINE_BLOCK.iteritems():
        html = re.sub(v, '\n', html)

    keeps = {}
    for img in re.findall(RE_IMG, html):
        md5 = hashlib.md5(img.encode('utf-8','ignore')).hexdigest()[:16]
        html = html.replace(img, md5)
        keeps[md5] = img
    for link in re.findall(RE_A, html):
        md5 = hashlib.md5(link.encode('utf-8','ignore')).hexdigest()[:16]
        html = html.replace(link, md5)
        keeps[md5] = link
    text = re.sub(RE_TAG, '', html)
    for md5, keep in keeps.iteritems():
        text = text.replace(md5, keep)
    text = unescape(text)
    lines = ["<p>"+x.strip()+"<\p>" for x in text.split("\n") if x.strip() != ""]
    return "\n".join(lines)

if __name__ == "__main__":
    html = open("1.html").read()
    ret = clean(html)
    print(ret)
