#!/usr/bin/env python

class Stack():
	def __init__(self):
		self.item = []
	def push(self,item):
		self.item.append(item)
		return self.item
	def pop(self):
		self.item.pop()
		return self.item
	
l1 = Stack()
print l1.push('abc')
