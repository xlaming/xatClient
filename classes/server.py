from os import path
from socket import *
from glob import glob
from select import select
from .config import Config
from .client import Client
from ntpath import basename
from threading import Thread
from .webserver import WebServer
from xml.etree.ElementTree import fromstring

class Server:
    def __init__(self):
        try:
            self.Threads = []
            self.Disabled = []
            self.WebServer = WebServer()
            self.RunServer = Thread(target=self.WebServer.start)
            self.RunServer.daemon = True
            self.RunServer.start()
            print("> Webserver started.")
            self.Plugins = []
            self.loadPlugins()
            print("> Plugins started.")
            self.RunSocket = Thread(target=self.createSocket)
            self.RunSocket.daemon = True
            self.RunSocket.start()
            print("> Socket started.")
        except:
            pass
    
    def createSocket(self):
        try:
            xSock = socket(AF_INET, SOCK_STREAM) 
            xSock.settimeout(None)
            xSock.bind((Config.CLIENT_SERVERIP, Config.CLIENT_SERVERPORT)) 
            xSock.listen(100) 
            while True: 
                (conn, (ip, port)) = xSock.accept()
                thread = Thread(target=Client, args=(self, conn))
                thread.daemon = True
                thread.start()
                self.Threads.append(thread) 
            for t in self.Threads: 
                t.join()
        except:
            pass

    def parsePlugins(self, packet, direction, user):
        for p in self.Plugins:
            exec(p, globals())
            data = plugin(self, packet, direction, user)
            if data:
                packet = data
        return packet

    def xml2Array(self, xml):
        try:
            returnArray = {}
            xml = xml.strip('\0')
            xml = fromstring(xml)
            returnArray['name'] = xml.tag
            for tag, attrib in xml.attrib.items():
                returnArray[tag] = attrib
        except: 
            pass
        return returnArray
    
    def buildPacket(self, node, packets):
        packet = ["<" + node]
        for (k, v) in packets.items():
            if str(k) != 'name':
                packet.append(str(k) + "=\"" + self.sanatize(str(v)) + "\"")
        packet.append("/>")
        return ' ' .join(packet) + '\x00'

    def fixUserID(self, uid):
        uid += "_"
        trim = uid.index('_')
        return uid[0:trim]
        
    def sanatize(self, data):
        entities = {
            '"': '&quot;', 
            '<': '&lt;', 
            '˃': '\xcb\x83'
        }
        for (i, u) in entities.items():
            data = data.replace(i, u)
        return data

    def loadPlugins(self):
        self.Plugins = []
        for pname in glob('plugins/*.py'):
            name = basename(pname).replace('.py', '')
            if not name in self.Disabled:
                self.Plugins.append(open(pname).read())

    def disablePlugin(self, name):
        if path.exists('plugins/' + name + '.py') and not name in self.Disabled:
            self.Disabled.append(name)
            self.loadPlugins()
            return True
        return False

    def enablePlugin(self, name):
        if name in self.Disabled:
            self.Disabled.remove(name)
            self.loadPlugins()
            return True
        return False