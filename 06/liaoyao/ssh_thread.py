#!/usr/bin/env python
#coding=utf-8

import socket
import logging
import sys
import threading

def handleconn(conn):
	addr = conn.getpeername()
	logging.info('accept from %s',addr)
	while True:
		#一次最多接收4096字节
		s = conn.recv(4096)
		#长度为0，表示接收完毕
		if len(s) == 0:
			break
		#将收到的数据发送回去
		conn.send(s)
	#关闭连接
	conn.close()
	logging.info('connection from %s closed',addr)

def main():
	if len(sys.argv) < 2:
		print 'usage: python echo_socket.py port'
		return
	FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
	logging.basicConfig(level=logging.DEBUG,format=FORMAT)
	#创建一个socket，AF_INET代表IPV4地址，SOCKET_STREAM代表TCP协议
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#重用socket地址
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	#绑定在指定的IP地址和端口上
	s.bind(('0.0.0.0',int(sys.argv[1])))
	#
	s.listen(3)
	logging.info('listening on 0.0.0.0:%s',sys.argv[1])
	while True:
		conn, addr = s.accept()
		t = threading.Thread(target=handleconn,args=(conn,))
		t.start()

if __name__ == '__main__':
	main()