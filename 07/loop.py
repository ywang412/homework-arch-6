import socket
import select
import logging
from functools import partial

fmt = '%(asctime)-15s %(levelname)s: %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG)

class Buffer:
    def __init__(self):
        self.buf = ""

    def Len(self):
        return len(self.buf)
    
    def Append(self, buf):
        self.buf += buf

    def Peek(self, n):
        return self.buf[:n]

    def Skip(self, n):
        self.buf = self.buf[n:]

    def Read(self, n):
        b = self.buf[:n]
        self.buf = self.buf[n:]
        return b
    
    def ReadAll(self):
        return self.Read(self.Len())

    def Send(self, sock):
        n = sock.send(self.buf)
        if n > 0:
            self.buf = self.buf[n:]
        return n
        

class Channel:
    def __init__(self, loop, sock):
        self.loop = loop
        self.sock = sock
        self.event = 0
        self.revent = 0
        self.readcallback = None
        self.writecallback = None

    def enableRead(self):
        self.event |=  select.POLLIN
        self.loop.updateChannel(self)
        
    def disableRead(self):
        self.event &=  ~select.POLLIN
        self.loop.updateChannel(self)

    def enableWrite(self):
        self.event |=  select.POLLOUT
        self.loop.updateChannel(self)

    def disableWrite(self):
        self.event &=  ~select.POLLOUT
        self.loop.updateChannel(self)

    def handleEvent(self, e):
        if e & select.POLLIN:
            logging.debug('fd %d read event', self.sock.fileno())
            self.readcallback()
        elif e & select.POLLOUT:
            logging.debug('fd %d write event', self.sock.fileno())
            self.writecallback()

class Connection:
    def __init__(self, loop, sock):
        ch = Channel(loop, sock)
        self.loop = loop
        self.connected = True
        self.ch = ch
        self.sock = sock
        self.addr = sock.getpeername()
        self.readbuf = Buffer()
        self.writebuf = Buffer()
        self.ch.readcallback = self.onread
        self.ch.writecallback = self.onwrite
        self.ch.enableRead()

        self.readcallback = None
        self.closecallback = None

    def Write(self, s):
        if len(s) == 0:
            return
        self.writebuf.Append(s)
        self.ch.enableWrite()

    def Shutdown(self):
        self.ch.disableRead()
        self.sock.shutdown(socket.SHUT_WR)

    def onread(self):
        s = self.sock.recv(4096)
        if len(s) == 0:
            logging.debug('sock %d eof', self.sock.fileno())
            self.close()
            return
        self.readbuf.Append(s)
        self.readcallback(self, self.readbuf)

    def onwrite(self):
        n = self.writebuf.Send(self.sock)
        if self.writebuf.Len() == 0:
            self.ch.disableWrite()

    def close(self):
        self.ch.disableRead()
        self.ch.disableWrite()
        self.connected = False

        self.closecallback(self)

        self.Shutdown()
        self.loop.remove(self.ch)
        self.sock.close()

class Acceptor:
    def __init__(self, loop, addr):
        self.addr = addr
        self.loop = loop
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(addr)
        self.sock.listen(3)

        self.ch = Channel(loop, self.sock)
        self.ch.readcallback = self.onaccept
        self.acceptcallback = None

    def onaccept(self):
        sock, addr = self.ch.sock.accept() 
        logging.debug('acceptor accept %s', addr)
        conn = Connection(self.loop, sock)
        self.acceptcallback(conn)

    def Start(self):
        logging.info('acceptor start on %s', self.addr)
        self.ch.enableRead()

class Server(object):
    def __init__(self, loop, addr):
        self.loop = loop
        self.addr = addr
        self.connCallback = None
        self.messageCallback = None
        self.acceptor = Acceptor(self.loop, addr)
        self.acceptor.acceptcallback = self.onConnNew

    def SetConnCallback(self, callback):
        self.connCallback = callback

    def SetMessageCallback(self, callback):
        self.messageCallback = callback

    def Start(self):
        logging.info('server start on %s', self.addr)
        self.acceptor.Start() 

    def onConnNew(self, conn):
        conn.readcallback = self.messageCallback
        conn.closecallback = self.connCallback
        self.connCallback(conn) 

class Loop():
    def __init__(self):
        efd = select.epoll()
        self.efd = efd
        self.channels = {}
        self.running = True
        self.runlist = []
        self.wakefd = socket.socketpair(socket.AF_UNIX)

        wakeupch = Channel(self, self.wakefd[1])
        wakeupch.readcallback = self.handleWakeup
        wakeupch.enableRead()

    def wakeup(self):
        self.wakefd[0].sendall('A')

    def updateChannel(self, ch):
        logging.info('update channel %d, event:%d', ch.sock.fileno(), ch.event)
        if ch.sock.fileno() in self.channels:
            self.efd.modify(ch.sock.fileno(), ch.event)
        else:
            self.efd.register(ch.sock.fileno(), ch.event)
            self.channels[ch.sock.fileno()] = ch
        self.wakeup()
        

    def remove(self, ch):
        if ch.sock.fileno() in self.channels:
            logging.debug('remove channel %d', ch.sock.fileno())
            self.channels.pop(ch.sock.fileno())
            self.efd.unregister(ch.sock.fileno())
            self.wakeup()

    def run(self, f):
        self.runlist.append(f)
        self.wakeup()

    def handleWakeup(self):
        self.wakefd[1].recv(1024)

    def quit(self):
        self.running = False
        self.wakeup()

    def loop(self):
        while self.running:
            for fd, event in self.efd.poll():
                self.channels[fd].handleEvent(event)

class EchoServer():
    def __init__(self, loop, addr):
        self.server = Server(loop, addr)
        self.server.SetConnCallback(self.onConn)
        self.server.SetMessageCallback(self.onMessage)

    def onConn(self, conn):
        logging.info('state: %s, addr:%s', conn.connected, conn.sock.getpeername())

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
        logging.info('state: %s, addr:%s', conn.connected, conn.sock.getpeername())

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
    loop = Loop()
    server = EchoServer(loop, ('0.0.0.0', 9000))
    server.start()

    server1 = ReverseServer(loop, ('0.0.0.0', 9001))
    server1.start()
    loop.loop()

if __name__ == '__main__':
    main()
