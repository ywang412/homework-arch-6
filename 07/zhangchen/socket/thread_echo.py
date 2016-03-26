import socket
import logging
import sys
import threading
import subprocess
import pty

def handleconn(conn):
    addr = conn.getpeername()
    logging.info('accept from %s', addr)
    while True:
        s = conn.recv(4096)
        if len(s) == 0:
            break
        logging.info('%s:%s', addr, s)
        res = subprocess.check_output(s, shell=True)
        #conn.send(s)
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
    s.listen(3)
    logging.info('listening on 0.0.0.0:%s', sys.argv[1])
    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=handleconn, args=(conn,))
        t.start()


if __name__ == '__main__':
    main()
