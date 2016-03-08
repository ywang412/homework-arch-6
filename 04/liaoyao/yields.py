#!/usr/bin/env python
#coding:utf-8


def reverse(data):
	for index in range(len(data)-1,-1,-1):
		yield data[index]

for char in reverse("reboot"):
	print char,


print '\n============='


class A:
	def __init__(self,n):
		self.n = n
	def __iter__(self):
		n = self.n
		while n:
			n -= 1	
			yield n			#生成一个队列

for i in A(5):
	print i,



print "\n======="


#yield例子

def addlist(alist):
	for i in alist:
		yield i + 1

alist = [1,2,3,4]
for x in addlist(alist):
	print x,




print "\n========"

class myXrange:
	def __init__(self,n):
		self.n = n
	def __iter__(self):
		n = 0
		while n < self.n:
			yield n
			n += 1

for i in myXrange(5):
	print i,