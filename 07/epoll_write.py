#!/user/bin/python
#encoding:utf8

import socket
import logging
import sys
import select
import os

class Connection:
    def __init__(self, sock):
        self.sock = sock
        self.buf = ""
        self.wbuf = ""

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
                conn.setblocking(1)
                logging.info('new connection %s, fd:%d', addr, conn.fileno())
                efd.register(conn.fileno(), select.POLLIN)
                person = Connection(conn)
                m[conn.fileno()] = person
            else:
                conn = m[fd]
                if event & socket.POLLOUT:
                    n = conn.sock.send(conn.wbuf)
                    if n < len(conn.wbuf):
                        conn.wbuf = conn.wbuf[n:] 
                    else:
                        conn.wbuf = ""
                        efd.modify(fd, socket.POLLIN)

                if event & socket.POLLIN:
                    buf, closed = readmsg(conn)
                    if closed:
                        efd.unregister(fd)
                        del m[fd]
                        conn.sock.close()
                        continue

                    if buf:
                        logging.debug('msg:"%s"', buf)
                        i = buf.find('\r')
                        name = buf[:i]
                        logging.debug('file name:%s', name)
                        conn.buf = ""

                        f = open(name)
                        s = f.read()
                        f.close()

                        n = conn.sock.send(s)
                        if len(n) < s:
                            conn.wbuf = s[n:]
                            event = socket.POLLIN | socket.POLLOUT
                            efd.modify(fd, event)

                        logging.debug('write %d', n)
                        conn.sock.shutdown(socket.SHUT_WR)
                        conn.sock.close()


if __name__ == '__main__':
    main()
