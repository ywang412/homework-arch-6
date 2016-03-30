#/usr/bin/env python
#coding=utf-8
#running on CentOS
import socket
import logging
import sys
import threading
import os
import select

def handleconn(conn):
    addr = conn.getpeername()
    logging.info('accept from %s', addr)
    while True:
        s = conn.recv(4096)
        if len(s) == 0:
            break
        logging.info('receive %s', s)
        conn.send(s)
    conn.close()
    logging.info('connection from %s closed', addr)

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
    efd.register(s.fileno(),select.POLLIN)

    #rl = [s.fileno()]
    #wl = []
    #xl = []
    m = {}
    while True:
        #logging.debug('input %s %s %s',rl,wl,xl)
        #rrl,wwl,xxl = select.select(rl,wl,xl)
        #logging.debug('output %s %s %s',rrl,wwl,xxl)
        l = efd.poll()
        logging.debug('output %s',l)
        for fd,event in l:
            if fd == s.fileno():
                conn,addr = s.accept()
                logging.info('new connection %s, fd:%d',addr,conn.fileno())
                #rl.append(conn.fileno())
                efd.register(conn.fileno(),select.POLLIN)
                m[conn.fileno()] = conn
            else:
                conn = m[fd]
                buf = conn.recv(4096)
                if len(buf) == 0:
                    logging.debug('fd %d eof',fd)
                    #rl.remove(fd)
                    del m[fd]
                    conn.close()
                    continue
                conn.send(buf)


if __name__ == '__main__':
    main()
