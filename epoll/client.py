from socket import *
import logging
import sys

FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
sock = create_connection(('127.0.0.1', 9000))

request = '{"cmd":"%s"}' %(sys.argv[1])
sock.send('%010d%s'%(len(request), request))
header = int(sock.recv(10))
body = sock.recv(header)
print body
sock.close()

