import socket
import logging
import sys
import threading

mutex = threading.Lock()
room = {}

def readmsg(conn):
    s = ""
    while True:
        c = conn.recv(1)
        if len(c) == 0:
            break
        s += c
        if c == '\n':
            break

    return s

def broadcast(msg):
    mutex.acquire()
    for conn in room:
        conn.send(msg)
    mutex.release()

def joinroom(conn):
    mutex.acquire()
    addr = '%s:%d'%(conn.getpeername())
    room[conn]=addr
    mutex.release()

def leaveroom(conn):
    mutex.acquire()
    #addr = '%s:%d'%(conn.getpeername())
    del room[conn]
    mutex.release()


def handleconn(conn):
    addr = '%s:%d'%(conn.getpeername())
    logging.info('accept from %s', addr)
    joinroom(conn)
    broadcast('%s join room\n' %(room[conn]))

    while True:
        s = readmsg(conn)
        if len(s) == 0:
            break
        logging.info('%s say "%s"', addr, s.strip('\n'))
        broadcast('%s:%s'%(room[conn], s))

    mess = room[conn]
    leaveroom(conn)
    broadcast('%s leave room\n' %(mess))
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
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
