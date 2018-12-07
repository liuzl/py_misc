import urllib3

from io import BytesIO
from http.client import HTTPResponse

class BytesIOSocket:
    def __init__(self, content):
        self.handle = BytesIO(content)

    def makefile(self, mode):
        return self.handle

def response_from_bytes(data):
    sock = BytesIOSocket(data)

    response = HTTPResponse(sock)
    response.begin()

    return urllib3.HTTPResponse.from_httplib(response)

if __name__ == '__main__':
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('httpbin.org', 80))
    sock.send(b'GET /gzip HTTP/1.1\r\nHost: httpbin.org\r\n\r\n')

    raw_response = sock.recv(8192)

    response = response_from_bytes(raw_response)
    print(response.headers)
    print(response.data)
