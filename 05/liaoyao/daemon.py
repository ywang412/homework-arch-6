#!/usr/bin/env python
#coding=utf-8


import sys,os,time,atexit
from signal import SIGTERM



class Daemon:

	def __init__(self,pidfile="nbMon.pid",stdin="/dev/null",stdout="nbMon.log",stderr="nbMon.log"):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile

	def daemonize(self):
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError,e:
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno,e.strerror))
			sys.exit(1)
		
		os.chdir("/")	#改变当前工作目录
		os.setsid()		#设置SID，成为session leader
		os.umask(0)		#重设umask


		#第二次fork
		try:
			pid = os.fork()
			if pid > 0:
				#父进程依然退出
				sys.exit(0)
		except OSError,e:
			sys.stderr.wirte("fork #2 failed: %d (%s)\n" % (e.errno,e.strerror))
			sys.exit(1)

		#重定向0，1，2三个FD(文件描述符),依次为标准输入、标准输出、错误输出
		#充电箱之前flush依次。确保该打印出来的文字已经输出
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin,'r')
		so = file(self.stdout,'a+')
		se = file(self.stderr,'a+',0)
		os.dup2(si.fileno(),sys.stdin.fileno())
		os.dup2(so.fileno(),sys.stdout.fileno())
		os.dup2(se.fileno(),sys.stderr.fileno())

		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)

	def delpid(self):
		os.remove(self.pidfile())

	def start(self):
		#检查pid文件是否存在，如果存在就认为程序还在运行
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if pid:
			message = "pidfile %s already exist. Daemon already running?\n"
			sys.stderr.write(message % self.pidfile)
			sys.exit(1)

		#开始变成守护进程
		self.daemonize()
		self.run()

	def stop(self):
		#从pid文件中获取进程id
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if not pid:
			message = "pidfile %s does not exist. Daemon not running?\n"
			sys.stderr.write(message % self.pidfile)
			return

		#开始c尝试kill掉守护进程
		try:
			while True:
				os.kill(pid,SIGTERM)
				time.sleep(0.1)
		except OSError,err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)

	def restart(self):
		self.stop()
		self.start()

	def run(self):
		pass