import socket
import ssl
import urllib.parse
import http.client
import os 
import random


b=["Mozilla/5.0","Mozilla/4.0","Mozilla/5.0 (Windows NT 10.0;Win64;x64)","Mozilla/5.0 (Windows NT 10.0;Win32)","Mozilla/5.0 (Macintosh;Intel Mac OS X 10_15_7)","Mozilla/5.0 (Linux;Android 10;Pixel 3 XL)","Mozilla/5.0 (Linux;Android 11;SM-G991B)","Mozilla/5.0 (iPhone;CPU iPhone OS 14_0 like Mac OS X)","Mozilla/5.0 (iPad;CPU OS 14_0 like Mac OS X)","Mozilla/5.0 (X11;Ubuntu;Linux x86_64;rv:89.0) Gecko/20100101 Firefox/89.0","Mozilla/5.0 (Windows NT 6.1;WOW64;rv:54.0) Gecko/20100101 Firefox/54.0","Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36","Mozilla/5.0 (Linux;Android 10;SM-G950F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"]
o=["Windows NT 10.0;Win64;x64","Windows NT 10.0;Win32","Macintosh;Intel Mac OS X 10_15_7","Linux;Android 10;Pixel 3 XL","Linux;Android 11;SM-G991B","iPhone;CPU iPhone OS 14_0 like Mac OS X","iPad;CPU OS 14_0 like Mac OS X","X11;Ubuntu;Linux x86_64","Windows NT 6.1;WOW64"]
e=["AppleWebKit/537.36 (KHTML, like Gecko)","Gecko/20100101","WebKit/605.1.15 (KHTML, like Gecko)","Trident/7.0;AS;rv:11.0","KHTML, like Gecko"]
v=["Chrome/91.0.4472.124","Chrome/92.0.4515.107","Firefox/89.0","Safari/537.36","Version/14.0.1","Version/14.0","Edge/92.0.902.62"]
UserAgent=f"{random.choice(b)} ({random.choice(o)}) {random.choice(e)} {random.choice(v)}"


class HTTPResponse:
    def __init__(self, status, headers, body, text):
        self.status = status
        self.headers = headers
        self.body = body
        self.text = text

class HTTPClient:
    def __init__(self, dns_server='xbox-dns.ru', user_agent=UserAgent, timeout=10):
        self.dns_server = dns_server
        self.user_agent = user_agent
        self.timeout = timeout

    def _resolve(self, host):
        return socket.gethostbyname(host)

    def request(self, method, url, headers=None, data=None):
        parsed = urllib.parse.urlparse(url)
        scheme = parsed.scheme
        host = parsed.hostname
        port = parsed.port or (443 if scheme == 'https' else 80)
        path = parsed.path or '/'
        if parsed.query:
            path += '?' + parsed.query
        headers = headers.copy() if headers else {}
        headers.setdefault('User-Agent', self.user_agent)
        ip = self._resolve(host)
        conn = None
        if scheme == 'https':
            context = ssl.create_default_context()
            conn = http.client.HTTPSConnection(ip, port, timeout=self.timeout, context=context)
        else:
            conn = http.client.HTTPConnection(ip, port, timeout=self.timeout)
        headers['Host'] = host
        conn.request(method, path, body=data, headers=headers)
        res = conn.getresponse()
        body = res.read()
        text = body.decode(errors='ignore')
        return HTTPResponse(res.status, dict(res.getheaders()), body, text)

    def get(self, url, headers=None):
        return self.request('GET', url, headers=headers)

    def post(self, url, headers=None, data=None):
        return self.request('POST', url, headers=headers, data=data)

_client = HTTPClient()

def get(url, headers=None):
    return _client.get(url, headers)

def post(url, headers=None, data=None):
    return _client.post(url, headers, data)
