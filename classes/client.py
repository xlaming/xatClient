from socket import *
from time import sleep
from select import select
from .config import Config
from threading import Thread

class Client:
    def __init__(self, server, sock):
        try:
            self.isConnected = False
            self.server = server
            self.socks = [[], []]
            self.users = {}
            self.userID = 0
            self.rank = 0
            self.chatID = 0
            self.socks[1] = sock
            self.connectToXat()
        except:
            pass

    def connectToXat(self):
        self.socks[0] = socket(AF_INET, SOCK_STREAM, SOL_TCP)
        self.socks[0].connect((Config.XAT_IP, Config.XAT_PORT))
        self.startHeartBeat()
        self.keepRunning()

    def keepRunning(self):
        try:
            while True:
                socks,_,_ = select(self.socks, [], []) 
                for sock in socks:
                    recv = ""
                    sock.setblocking(0)
                    while recv[-1:] != chr(0):
                        recv += sock.recv(2048).decode('utf-8', 'ignore')
                        if len(recv) < 1:
                            self.killSockets()
                            break
                    if recv:
                        for packet in recv.split('\x00'):
                            if '<f ' in packet:
                                dataInfo = 1 if sock == self.socks[0] else 0
                                self.socks[dataInfo].send(bytes(packet + '\x00', encoding='utf-8'))
                            else:
                                self.parse(sock, packet)
        except:
            self.killSockets()

    def parse(self, sock, packet):
        data = self.server.xml2Array(packet)
        if not data:
            return
        dataInfo = [1, 'fromxat', 'RECV'] if sock == self.socks[0] else [0, 'toxat', 'SENT']
        data = self.server.parsePlugins(data, dataInfo[1], self)
        if data['name'] == 'policy-file-request':
            self.sendToUser(Config.CROSSDOMAIN)
        elif data['name'] != 'HIDDEN':
            if data['name'] == 'j2':
                self.userID = int(data['u'])
                self.chatID = int(data['c'])
            elif data['name'] == 'i' and 'r' in data:
                self.rank = int(data['r'])
            elif data['name'] == 'l' and 'u' in data:
                if int(data['u']) in self.users:
                    del self.users[int(data['u'])]
            elif data['name'] == 'done':
                self.isConnected = True
                self.announce('xatClient is running...')
            elif data['name'] == 'u' and 'u' in data:
                self.users[int(data['u'])] = {
                    'name': data['n'],
                    'avatar': data['a'],
                    'home': data['h'],
                     'rank': int(data['f']) & 7 if 'f' in data else 5,
                    'reg': data['N'] if 'N' in data else False,
                    'd0': data['d0'] if 'd0' in data else False,
                    'd2': data['d2'] if 'd2' in data else False,
                    'f': data['f'] if 'f' in data else False,
                }
            toBeSend = self.server.buildPacket(data['name'], data)
            print('[' + dataInfo[2] + ' - ' + str(self.chatID) + ']: ', toBeSend)
            self.socks[dataInfo[0]].send(bytes(toBeSend, encoding='utf-8'))

    def sendToUser(self, packet):
        print('[RECV - ' + str(self.chatID) + ']: ', packet)
        return self.socks[1].send(bytes(packet + '\x00', encoding='utf-8'))

    def sendToXat(self, packet):
        print('[SENT - ' + str(self.chatID) + ']: ', packet)
        return self.socks[0].send(bytes(packet + '\x00', encoding='utf-8'))

    def announce(self, message):
        self.sendToUser(self.server.buildPacket('m', {'t': message, 'u': 0}))

    def killSockets(self):
        for sock in self.socks:
            sock.close()

    def sendHeartBeat(self):
        try:
            sleep(10) # first time only
            while True:
                if self.isConnected:
                    self.sendToXat(self.server.buildPacket('c', {'u': self.userID, 't': '/KEEPALIVE'}))
                    sleep(50)
        except:
            pass


    def startHeartBeat(self):
        thread = Thread(target=self.sendHeartBeat)
        thread.daemon = True
        thread.start()

    def getById(self, userid):
        if not self.users:
            return False
        for uid, user in self.users.items():
            if userid == uid:
                return user
        return False 