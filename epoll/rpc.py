from loop import *
from buffer import *
import json
import subprocess

class RpcServer():
    def __init__(self, loop, addr, handler):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)
        self.handler = handler

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
                response = self.handler(body)
                conn.Write('%010d%s'%(len(response), response))

    def start(self):
        self.server.Start()

def handler(msg):
    '''
    {
        "cmd":""
    }
    '''
    d = json.loads(msg)
    cmd = d["cmd"]
    out = subprocess.check_output(cmd, shell=True)
    return out

def main():
    fmt = '%(asctime)-15s %(levelname)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)
    loop = Loop()
    server = RpcServer(loop, ('0.0.0.0', 9000), handler)
    server.start()

    loop.loop()

if __name__ == '__main__':
    main()
