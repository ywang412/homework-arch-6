from loop import *
from resp import *

class RedisServer():
    def __init__(self, loop, addr):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)
        self.stat = State()
        self.m = {}

    def onConn(self, conn):
        logging.info('state: %s, addr:%s', conn.connected, conn.Remote())

    def onMessage(self, conn, buf):
        self.stat = readMessage(buf, self.stat)
        while self.stat.done:
            l = self.stat.data
            method = l[0].upper()
            if method == 'GET':
                logging.debug('key:"%s"', l[0])
                conn.Write(writeMessage(self.m.get(l[1], None)))
            elif method == 'SET':
                logging.debug('key:"%s", value:"%s"', l[0], l[1])
                self.m[l[1]] = l[2]
                conn.Write(writeMessage('OK'))
            self.stat = readMessage(buf, State())


    def start(self):
        self.server.Start()

loop = Loop()
server = RedisServer(loop, ('0.0.0.0', 9000))
server.start()
loop.loop()
