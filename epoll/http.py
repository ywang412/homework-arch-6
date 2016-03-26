from loop import *

class HTTPServer():
    def __init__(self, loop, addr):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)

    def onConn(self, conn):
        logging.info('state: %s, addr:%s', conn.connected, conn.Remote())

    def onMessage(self, conn, buf):
        s = buf.ReadUtil('\r\n\r\n')
        if len(s) == 0:
            return
        i = s.find('\r\n')
        name = s[:i].split(' ')[1]

        code = 200
        res = ""
        try:
            f = open('.' + name)
            res = f.read()
            f.close()
        except Exception, e:
            conn.Write('HTTP/1.1 404 not found\r\n\r\n') 

        logging.info('code:%d', code)
        if code == 200:
            conn.Write('HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s\r\n'%(
             len(res), res))
        conn.Shutdown()


    def start(self):
        self.server.Start()

def main():
    fmt = '%(asctime)-15s %(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)

    loop = Loop()
    server = HTTPServer(loop, ('0.0.0.0', 9000))
    server.start()
    loop.loop()

if __name__ == '__main__':
    main()
