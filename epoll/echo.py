from loop import *
from buffer import *

class EchoServer():
    def __init__(self, loop, addr):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)

    def onConn(self, conn):
        logging.info('state: %s, addr:%s', conn.connected, conn.Remote())

    def onMessage(self, conn, buf):
        conn.Write(buf.ReadAll())

    def start(self):
        self.server.Start()

class ReverseServer():
    def __init__(self, loop, addr):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)

    def onConn(self, conn):
        logging.info('state: %s, addr:%s', conn.connected, conn.Remote())

    def onMessage(self, conn, buf):
        while True:
            if buf.Len() < 10:
                return
            else:
                n = int(buf.Peek(10))
                if buf.Len() < 10 + n:
                    return
                buf.Skip(10)
                body = buf.Read(n)
                logging.debug('send %s', body)
                conn.Write('%010d'%(n))
                conn.Write(body[::-1])

    def start(self):
        self.server.Start()

def main():
    fmt = '%(asctime)-15s %(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    loop = Loop()
    server = EchoServer(loop, ('0.0.0.0', 9000))
    server.start()

    server1 = ReverseServer(loop, ('0.0.0.0', 9001))
    server1.start()
    loop.loop()

if __name__ == '__main__':
    main()
