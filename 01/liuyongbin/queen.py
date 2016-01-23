#!/usr/bin/env python
class queen(object):
    emptyqueen=[]
    def push(self,message):
        self.emptyqueen.append(message)
    def pop(self):
        print self.emptyqueen.pop()
class stack(object):
    emptyqueen=[]
    def push(self,message):
        self.emptyqueen.append(message)
    def pop(self):
        print self.emptyqueen.pop(0)
