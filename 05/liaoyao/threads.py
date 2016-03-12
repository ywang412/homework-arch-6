#!/usr/bin/env python

#coding: utf-8

import thread


def f(name):
	print "This is " + name


if __name__ == '__main__':
	thread.start_new_thread(f,("thread1",))

	while 1:
		pass