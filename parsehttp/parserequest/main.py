from urllib.parse import parse_qs

def parse_post(requestline):
    requestline = requestline.rstrip('\r\n')
    try:
        rawheaders, body = requestline.split("\r\n\r\n", 1)
        items = rawheaders.split("\r\n")
        if len(items) < 1: return False
        method, path, version = items[0].split(" ")
        headers = {}
        for item in items[1:]:
            k,v = item.split(": ")
            headers[k] = v
        post = parse_qs(body)
        ret = {
            "method": method,
            "path": path,
            "version": version,
            "headers": headers,
            "body": post,
        }
        return ret
    except:
        return False

if __name__ == "__main__":
    from text import *
    ret = parse_post(text)
    print(ret)
