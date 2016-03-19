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
    for addr in room:
        c = room[addr]
        c.send(msg)
    mutex.release()

def joinroom(conn):
    mutex.acquire()
    addr = '%s:%d'%(conn.getpeername())
    room[addr]=conn
    mutex.release()

def leaveroom(conn, name=None):
    if name:
        mutex.acquire()
        del room[name]
        mutex.release()
    else:
        mutex.acquire()
        addr = '%s:%d'%(conn.getpeername())
        del room[addr]
        mutex.release()


def handleconn(conn):
    addr = '%s:%d'%(conn.getpeername())
    logging.info('accept from %s', addr)
    joinroom(conn)
    broadcast('%s join room\n' %(addr))

    while True:
        s = readmsg(conn)
        if len(s) == 0:
            break
        if s.rstrip('\n') == 'name=admin&password=admin':
            if vars().has_key('name'):
                old_name = name
                name = 'admin'
                room[name] = room[old_name]
                del room[old_name]
            else:
                name = 'admin'
                room[name] = room[addr]
                del room[addr]
        elif s[:3] == 'del':
            someone = s[4:].rstrip('\n')
            if someone in room and name == 'admin':
                room[someone].close()
                leaveroom(room[someone],someone)
                logging.info('del "%s"', someone)
                broadcast('del %s'%(someone))
        elif s[:5] == 'name=':
            if vars().has_key('name'):
                old_name = name
                name = s[5:].rstrip('\n')
                if name =='admin':
                    name = old_name
                    continue
                room[name] = room[old_name]
                del room[old_name]
            else:
                name = s[5:].rstrip('\n')
                room[name] = room[addr]
                del room[addr]
        if vars().has_key('name'):
            logging.info('%s say "%s"', name, s.strip('\n'))
            broadcast('%s:%s'%(name, s))
        else:
            logging.info('%s say "%s"', addr, s.strip('\n'))
            broadcast('%s:%s'%(addr, s))

    if vars().has_key('name'):
        leaveroom(conn, name)
        logging.info('%s leave room\n' %(name))
        broadcast('%s leave room\n' %(name))
        conn.close()
        logging.info('connection from %s closed', name)
    else:
        leaveroom(conn)
        logging.info('%s leave room\n' %(addr))
        broadcast('%s leave room\n' %(addr))
        conn.close()
        logging.info('connection from %s closed', addr)

def main():
    if len(sys.argv) < 2:
        print 'usage python chat.py port'
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
