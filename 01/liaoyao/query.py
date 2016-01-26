#!/usr/bin/env python

class Query():
	def __init__(self):
		self.item =  []
	def push(self,value):
		self.item.append(value)
		return self.item
	def pop(self):
		tmp = self.item[1:]
		del self.item
		return tmp

l1 = Query()
l1.push(1)
l1.push(2)
print l1.pop()
