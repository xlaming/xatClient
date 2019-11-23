from re import *
from socket import *
from requests import *
from json import dumps
from .config import Config

class WebServer:
    def __init__(self):
        self.sendHeaders = "HTTP/1.1 200 OK\nContent-Type: {}\n\n"
        self.ip2Cached = False

    def start(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((Config.WEB_SERVERIP, Config.WEB_SERVERPORT))
        self.sock.listen(25)
        while(True):
            usock, address = self.sock.accept()
            recv = usock.recv(4096)
            if recv:
                URI = self.parseUrl(recv)
                if '/ip2.php' in URI:
                    self.send(usock, self.getIP2(), 'application/json')
                elif '/crossdomain.xml' in URI:
                    self.send(usock, Config.CROSSDOMAIN, 'text/xml')
                else:
                    self.send(usock, 'xatClient is running...', 'text/hhtml')
        self.sock.close()

    def send(self, usock, text, mime):
        usock.send((self.sendHeaders.format(mime) + text + "\n").encode('utf-8'))
        usock.shutdown(SHUT_WR)
        usock.close()

    def getIP2(self):
        if not self.ip2Cached:
            source = get('https://xat.com/web_gear/chat/ip2.php')
            replace = source.json()
            replace['E0'] = [1, ['127.0.0.1:' + str(Config.CLIENT_SERVERPORT) + ':1']]
            replace['E1'] = [1, ['127.0.0.1:' + str(Config.CLIENT_SERVERPORT) + ':1']]
            self.ip2Cached = dumps(replace)
        return self.ip2Cached

    def parseUrl(self, headers):
        parseHeaders = headers.decode()
        parseGET = findall("GET (.*?) ", parseHeaders)
        if not parseGET:
            return '/'
        return parseGET[0]