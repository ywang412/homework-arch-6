import os
import sys
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 9000))
sock.listen(4)
l = []
for i in range(3):
    pid = os.fork()
    if pid == 0:
        cnt = 0
        while True:
            conn, addr = sock.accept()
            print 'pid %d accept %s' %(os.getpid(), addr)
            conn.close()
            cnt += 1
            if cnt == 2:
                sock.close()
                sys.exit(0)
    else:
        l.append(pid)

sock.close()
for pid in l:
    pid, stat = os.wait()
    print 'pid %d exit code %d' %(pid, stat)

