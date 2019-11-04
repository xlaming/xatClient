from socket import *
from glob import glob
from select import select
from .config import Config
from threading import Thread
from .webserver import WebServer
from xml.etree.ElementTree import fromstring

class Client:
    def __init__(self):
        self.Threads = []
        self.WebServer = WebServer()
        self.RunServer = Thread(target=self.WebServer.start)
        self.RunServer.daemon = True
        self.RunServer.start()
        print("> Webserver started.")
        self.RunSocket = Thread(target=self.createSocket)
        self.RunSocket.daemon = True
        self.RunSocket.start()
        print("> Socket started.")
    
    def createSocket(self):
        try:
            xSock = socket(AF_INET, SOCK_STREAM) 
            xSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
            xSock.bind((Config.CLIENT_SERVERIP, Config.CLIENT_SERVERPORT)) 
            while True: 
                xSock.listen(4) 
                (conn, (ip, port)) = xSock.accept()
                thread = Thread(target=self.addClient, args=(conn,))
                thread.start() 
                self.Threads.append(thread) 
            for t in self.Threads: 
                t.join() 
        except:
            pass

    def parsePlugins(self, packet, direction, sock):
        for pname in glob('plugins/*.py'):
            exec(open(pname).read(), globals())
            data = plugin(self, packet, direction, sock)
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
                packet.append(str(k) + "=\"" + str(v) + "\"")
        packet.append("/>")
        return (' ' .join(packet) + '\x00').encode()

    def fixUserID(self, uid):
        uid += "_"
        trim = uid.index('_')
        return uid[0:trim]

    def addClient(self, conn):
        socks = [[], []]
        socks[0] = socket(AF_INET, SOCK_STREAM, SOL_TCP)
        socks[0].connect((Config.XAT_IP, Config.XAT_PORT))
        socks[1] = conn
        try:
            while True:
                allSocks,_,_ = select(socks, [], []) 
                for sock in allSocks:
                    recv = ""
                    while recv[-1:] != chr(0):
                        recv += sock.recv(2048).decode('utf8')
                        if len(recv) <= 1:
                            break
                    if recv:
                        for packet in recv.split('\x00'):
                            data = self.xml2Array(packet)
                            if data:
                                dataInfo = [1, 'fromxat', 'RECV'] if sock == socks[0] else [0, 'toxat', 'SENT']
                                data = self.parsePlugins(data, dataInfo[1], conn)
                                toBeSend = self.buildPacket(data['name'], data)
                                if data['name'] == 'policy-file-request':
                                    socks[1].send(Config.CROSSDOMAIN.encode() + b'\x00')
                                elif data['name'] != 'HIDDEN':
                                    print('[' + dataInfo[2] + ']: ' + toBeSend.decode('utf-8'))
                                    socks[dataInfo[0]].send(toBeSend)
        except:
            socks[0].close()
            socks[1].close()
        
