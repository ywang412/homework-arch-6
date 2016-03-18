#!/usr/bin/env python
# encoding: utf-8

import sys
import logging
import threading
import socket
import time
def handleconn(conn, ip):
    addr = conn.getpeername()
    logging.info('accept from {addr}'.format(addr=addr))
    name = ''
    while True:
        if not name:
            conn.send('Please input your name:')
            name = conn.recv(4096).strip('\n')
            if name == 'admin':
                conn.send('Please input your pas:')
                pas = conn.recv(4096).strip('\n')
                if pas == '123':
                    print 'welcome admin,you can use kill port'
                    s = conn.recv(4096).strip('\n')
                    if s == 'kill':
                        print 'print input port'
                        global killport
                        killport = conn.recv(4096).strip('\n')
                        time.sleep(6)
                        if int(killport) == ip[1]:
                            exit(0)
            else:
                if  killport == ip[1]:
                    sys.exit()
                s = conn.recv(4096)
        if len(s) == 0:
            break
        logging.info('user:{name} receive:{s}'.format(name=name,s=s))
        conn.send(s)
    conn.close()
    logging.info('connection from {addr} closed'.format(addr=addr))

def main():
    if len(sys.argv) < 2:
        print 'usage python echo.py port'
        return
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=FORMAT)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#IPV4地址，TCP协议
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)#不需要4分钟保护机制，否则端口会被占用，DEBUG用，重用socket地址
    s.bind(('0.0.0.0',int(sys.argv[1])))
    s.listen(3)
    logging.info('listening on 0.0.0.0:{port}'.format(port=sys.argv[1]))
    global killport
    while True:
        conn, addr = s.accept()
#        handleconn(conn)
        t = threading.Thread(target=handleconn, args=(conn,addr))
        t.start()

if __name__ == '__main__':
    main()
