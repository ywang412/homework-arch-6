# -*- coding: utf-8 -*-
class mylist:
    def __init__(self):
        self.mylist = []
    def push(self, word):
        self.mylist.append(word)
    def pop(self):
        self.mylist.pop(0)
    def show(self):
        print self.mylist

