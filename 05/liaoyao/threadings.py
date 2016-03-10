#!/usr/bin/env python
#coding=utf-8


import threading
import time

class Th(threading.Thread):
	def __init__(self,thread_name):
		threading.Thread.__init__(self)
		self.setName(thread_name)

	def run(self):
		print "This is thread " + self.getName()
		for i in range(5):
			time.sleep(1)
			print str(i)
		print self.getName() + "is over"


#join()阻塞等待
if __name__ == '__main__':
	thread1 = Th("T1")
	thread1.start()
	#thread1.join()
	print "main thread is over"