#!/usr/bin/env python
# encoding: utf-8

from socket import *
import threading

def thread(sock):
    while True:
        s = sock.recv(10)
        print 'thread',s

pipe = socketpair(AF_UNIX)#创建管道
threading.Thread(target=thread,args=(pipe[1],)).start()
while True:
    s = raw_input()
    pipe[0].send(s)
