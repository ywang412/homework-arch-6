#!/user/bin/python
#encoding:utf8

import socket
import logging
import sys
import select
import os

room = {}

def sendall(s, who):
    for name in room:
        conn = room[name]
        whoname = '%s:%d'%(who.sock.getpeername())
        conn.sock.send('%s %s'%(whoname, s))

def join(conn):
    name = '%s:%d'%(conn.sock.getpeername())
    room[name] = conn

def leave(conn):
    name = '%s:%d'%(conn.sock.getpeername())
    del room[name]

class Connection:
    def __init__(self, sock):
        self.sock = sock
        self.buf = ""

# (msg, closed)
def readmsg(conn):
    s = conn.sock.recv(4096)
    if len(s) == 0:
        return (conn.buf, True)
    logging.debug('recv "%s"', s)
    conn.buf += s
    if conn.buf.find('\n') != -1:
        return (conn.buf, False)
    else:
        return (None, False)

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

    efd = select.epoll()
    efd.register(s.fileno(), select.POLLIN)
    m = {}
    while True:
        l = efd.poll()
        logging.debug('output %s', l)
        for fd, event in l:
            if fd == s.fileno():
                conn, addr = s.accept()
                logging.info('new connection %s, fd:%d', addr, conn.fileno())
                efd.register(conn.fileno(), select.POLLIN)
                person = Connection(conn)
                m[conn.fileno()] = person
                join(person)
            else:
                conn = m[fd]
                buf, closed = readmsg(conn)
                if closed:
                    leave(conn)
                    logging.debug('fd %d eof', fd)
                    efd.unregister(fd)
                    del m[fd]
                    conn.sock.close()
                    continue

                if buf:
                    sendall(buf, conn)
                    conn.buf = ""


if __name__ == '__main__':
    main()
