import socket
import logging
import sys
import threading

mutex = threading.Lock()
room = {}
nameset = set()
moot = {}

def readmsg(conn):
    s = ""
    while True:
        try:
            c = conn.recv(1)
        except socket.error:
            s = ""
            break
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
    del moot[room[conn]]
    nameset.remove(room[conn])
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
        elif s[:9] == '--rename:':
            s = s.strip()
            if s[9:] in nameset:
                conn.send("reject rename\n")
            else:
                if room[conn] in nameset:
                    nameset.remove(room[conn])
                    del moot[root[conn]]
                nameset.add(s[9:])
                broadcast("%s change name to %s\n" % (room[conn], s[9:]))
                room[conn] = s[9:]
                moot[s[9:]] = conn
            continue
        elif s[:7] == "--kick:":
            s = s.strip()
            if s[7:] in nameset:
                kickconn = moot[s[7:]]
                kickconn.send("You have benn booted!\n")
                leaveroom(kickconn)
                kickconn.close()
            else:
                conn.send("%s not found\n" % (s[7:]))
            continue
        else:
            logging.info('%s say "%s"', addr, s.strip('\n'))
            if room.get(conn, None):
                broadcast('%s:%s'%(room[conn], s))

    if room.get(conn, None):
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
