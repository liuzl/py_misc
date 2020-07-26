from os import getenv
import requests

def get_duckling_url():
    url = getenv("DUCKLING_URL")
    if isinstance(url, str):
        return url
    return "http://127.0.0.1:8000/parse"

def get_duckling_locale():
    locale = getenv("DUCKLING_LOCALE")
    if isinstance(locale, str):
        return locale
    return 'zh_CN'

def get_duckling_tz():
    tz = getenv("DUCKLING_TZ")
    if isinstance(tz, str):
        return tz
    return 'Asia/Shanghai'

class Duckling(object):
    def __init__(self,
            locale=get_duckling_locale(),
            url=get_duckling_url(),
            tz=get_duckling_tz()):
        self.locale = locale
        self.url = url
        self.tz = tz

    def __call__(self, text, locale=None, tz=None):
        return self.request(text, locale, tz)

    def request(self, text, locale=None, tz=None):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        ret = requests.post(self.url, headers=headers,
                data={"text":text, "locale":locale or self.locale, "tz":tz or self.tz})
        if ret.status_code == 200:
            return ret.json()
        return []


if __name__ == "__main__":
    duckling = Duckling()
    text = "我打算明天下午三点去清华智源中心，可能需要开车十五公里"
    ret = duckling(text)
    import json
    print(json.dumps(ret, ensure_ascii=False))
