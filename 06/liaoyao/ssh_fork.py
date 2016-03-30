#/usr/bin/env python
#coding=utf-8

import socket
import logging
import sys
import os
import signal
import errno

def handleconn(conn):
	addr = conn.getpeername()
	logging.info('accept from %s',addr)
	while True:
		s = conn.recv(4096)
		if len(s) == 0:
			break
		conn.send(s)
	conn.close()
	logging.info('connection from %s closed',addr)

def handlesig(num, frame):
    pid, stat = os.wait()
    logging.info('pid %s exit, code %d', pid, stat)

def main():
	if len(sys.argv) < 2:
		print 'usage: python %s port' % sys.argv[0]
		return

	# handle signal
    signal.signal(signal.SIGCHLD, handlesig)
    
	#handle signal
	FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
	logging.basicConfig(level=logging.DEBUG,format=FORMAT)

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(('0.0.0.0',int(sys.argv[1])))
	s.listen(3)
	logging.info('listening on 0.0.0.0:%s',sys.argv[1])
	while True:
		try:
			conn,addr = s.accept()
		except socket.error,e:
			if e.errno == errno.EINTR:
				continue
			else:
				logging.error(e)
				break
		pid = os.fork()
		if pid == 0:
			s.close()
			handleconn(conn)
			sys.exit(0)
		conn.close()

if __name__ == '__main__':
	main()