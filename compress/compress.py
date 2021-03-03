import base64
import zlib

def encode(content):
    return base64.b64encode(zlib.compress(content))

def decode(s):
    return zlib.decompress(base64.b64decode(s))

if __name__ == "__main__":
    raw = b"123123123" * 100
    print(len(raw))
    enc = encode(raw)
    print(len(enc))
    print(enc)
    dec = decode(enc)
    print(dec)
    assert raw == dec
