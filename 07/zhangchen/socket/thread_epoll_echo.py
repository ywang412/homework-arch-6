#!/user/bin/python
#encoding:utf8

import socket
import logging
import sys
import select
import os
import threading

class Loop:
    def __init__(self, pipe, name='ioloop'):
        self.name = name
        self.pipe = pipe
        self.efd = select.epoll()
        self.m = {}

        self.efd.register(pipe.fileno(), select.POLLIN)#注册文件描述符和POLLIN读取数据事件i在服务端socket上面注册对读event的关注。
                                                       #一个读event随时会触发服务端socket去接收一个socket连接

    def loop(self):
        while True:
            for fd, event in self.efd.poll():#查询epoll对象，看是否有任何关注的event被触发。参数“1”表示，我们会等待1秒来看是否有event发生。
                                             #如果有任何我们感兴趣的event发生在这次查询之前，这个查询就会带着这些event的列表立即返回。
                if fd == self.pipe.fileno():
                    newfd = int(self.pipe.recv(4))
                    logging.info('%s receive new fd %d', self.name, newfd)
                    self.m[newfd] = socket.fromfd(newfd, socket.AF_INET, socket.SOCK_STREAM)#用文件描述符实例化一个socket网络对象用来接收用户请求
                    self.efd.register(newfd, select.POLLIN)
                else:
                    conn = self.m[fd]
                    buf = conn.recv(4096)
                    if len(buf) == 0:
                        logging.debug('fd %d eof', fd)
                        self.efd.unregister(fd)
                        del self.m[fd]
                        conn.shutdown(socket.SHUT_WR)
                        conn.close()
                        continue
                    conn.send(buf)

def main():
    if len(sys.argv) < 2:
        print 'usage python echo.py port'
        return
    FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#建立socket对象
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)#设置socket选项,var1定义了哪个选项将被使用,var2根据一设置一些选项，var3设置选项为True
    s.bind(('0.0.0.0', int(sys.argv[1])))#绑定到一个端口（也可以是一个指定的网卡）
    s.listen(1)#侦听连接
    logging.info('listening on 0.0.0.0:%s', sys.argv[1])

    pipes = []
    for i in range(4):
        pipe = socket.socketpair(socket.AF_UNIX)#创建一个Unix进程间通信的一对文件描述符
        loop = Loop(pipe[1], 'loop' + str(i))
        pipes.append(pipe[0])
        thread = threading.Thread(target=loop.loop)
        thread.setDaemon(True)
        thread.start()

    i = 0
    while True:
        conn, addr = s.accept()
        pipe = pipes[i]
        i = (i + 1)%len(pipes)
        sfd = '%04d' %(os.dup(conn.fileno()))
        pipe.send(sfd)
        conn.close()
        conn = None

if __name__ == '__main__':
    main()
