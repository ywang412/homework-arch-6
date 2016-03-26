#!/user/bin/python
#encoding:utf8

import socket
import logging
import sys
import select
import os
import threading

mutex = threading.Lock()
room = {}

def broadcast(msg):
    mutex.acquire()
    for addr in room:
        c = room[addr]
        c.send(msg)
    mutex.release()

def joinroom(conn):
    mutex.acquire()
    addr = '%s:%d'%(conn.getpeername())
    room[addr]=conn
    mutex.release()

def leaveroom(conn):
    mutex.acquire()
    addr = '%s:%d'%(conn.getpeername())
    del room[addr]
    mutex.release()


class Loop:
    def __init__(self, pipe, name='ioloop'):
        self.name = name
        self.pipe = pipe
        self.efd = select.epoll()
        self.m = {}

        self.efd.register(pipe.fileno(), select.POLLIN)

    def loop(self):
        while True:
            for fd, event in self.efd.poll():
                if fd == self.pipe.fileno():
                    newfd = int(self.pipe.recv(4))
                    logging.info('%s receive new fd %d', self.name, newfd)
                    self.m[newfd] = socket.fromfd(newfd, socket.AF_INET, socket.SOCK_STREAM)
                    conn = self.m[newfd]
                    addr = '%s:%d'%(conn.getpeername())
                    logging.info('accept from %s', addr)
                    joinroom(conn)
                    broadcast('%s join room\n' %(addr))
                    self.efd.register(newfd, select.POLLIN)
                else:
                    conn = self.m[fd]
                    addr = '%s:%d'%(conn.getpeername())
                    buf = conn.recv(4096)
                    if len(buf) == 0:
                        logging.debug('fd %d eof', fd)
                        self.efd.unregister(fd)
                        del self.m[fd]
                        leaveroom(conn)
                        conn.shutdown(socket.SHUT_WR)
                        broadcast('%s leave room\n' %(addr))
                        conn.close()
                        logging.info('connection from %s closed', addr)
                        continue
                    broadcast('%s:%s'%(addr, buf))
                    logging.info('%s say "%s"', addr, buf.rstrip())

def main():
    if len(sys.argv) < 2:
        print 'usage python echo.py port'
        return
    FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', int(sys.argv[1])))
    s.listen(1)
    logging.info('listening on 0.0.0.0:%s', sys.argv[1])

    pipes = []
    for i in range(4):
        pipe = socket.socketpair(socket.AF_UNIX)
        loop = Loop(pipe[1], 'loop' + str(i))
        pipes.append(pipe[0])
        thread = threading.Thread(target=loop.loop)
        thread.setDaemon(True)
        thread.start()

    i = 0
    while True:
        conn, addr = s.accept()
        pipe = pipes[i]
        i = (i + 1)%len(pipes)
        sfd = '%04d' %(os.dup(conn.fileno()))
        pipe.send(sfd)
        conn.close()
        conn = None

if __name__ == '__main__':
    main()
