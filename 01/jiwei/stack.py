# -*- coding: utf-8 -*-
class stack:
    def __init__(self):
        self.stack = []
    def push(self, word):
        self.stack.append(word)
    def pop(self):
        self.stack.pop()
    def show(self):
        print self.stack

