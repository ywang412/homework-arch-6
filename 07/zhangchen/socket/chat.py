import socket
import logging
import sys
import threading

mutex = threading.Lock()
room = {}

class Person:
    def __init__(self, name, conn):
        self.name = name
        self.conn = conn

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
    for name in room:
        p = room[name]
        p.conn.send(msg)
    mutex.release()

def joinroom(p):
    mutex.acquire()
    room[p.name]=p
    mutex.release()

def leaveroom(p):
    mutex.acquire()
    del room[p.name]
    mutex.release()

def killperson(name):
    mutex.acquire()
    p = room.get(name, None)
    if not p:
        logging.info("%s not found", name)
    else:
        p.conn.send('killed by admin')
        p.conn.shutdown(socket.SHUT_RD) 
    mutex.release()


def handleconn(conn):
    addr = '%s:%d'%(conn.getpeername())
    logging.info('accept from %s', addr)

    # read name
    name = readmsg(conn).strip('\n')
    p = Person(name, conn)

    joinroom(p)
    broadcast('%s join room, from %s\n' %(name, addr))

    while True:
        s = readmsg(conn)
        if len(s) == 0:
            break
        if name == 'admin':
            l = s.strip('\n').split(' ')
            if len(l) == 2 and l[0] == 'kill':
                killperson(l[1])
                continue
        logging.info('%s say "%s"', name, s.strip('\n'))
        broadcast('%s:%s'%(name, s))

    leaveroom(p)
    broadcast('%s leave room\n' %(name))
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
