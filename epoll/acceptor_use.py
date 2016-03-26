from loop import *

def printConn(conn):
    print conn.Remote()
    conn.Write('hello')
    conn.Shutdown()

fmt = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG)

loop = Loop()
acceptor = Acceptor(loop, ('0.0.0.0', 9000))
acceptor.acceptcallback = printConn
acceptor.Start()
loop.loop()
