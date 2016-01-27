#!/usr/bin/python
# -*- coding: utf-8 -*-
class Stack(object):
    
    def __init__(self, size=8):
        self.__stack = []
        self.__size = size
        self.__top = -1

    def isfull(self):
        if self.__top+1 == self.__size:
            return True
        else:
            return False

    def isempty(self):
        if self.__top == -1:
            return True
        else:
            return False

    def push(self, data):
        if self.isfull():
            raise Exception('Error, Stack Over Flow.')
        else:
            self.__top += 1
            self.__stack.append(data)

    def pop(self):
        if self.isempty():
            raise Exception('Error, Stack is Empty.')
        else:
            self.__top -= 1
            self.__stack.pop()

    def top(self):
        if self.isempty():
            raise Exception('Error, Stack is Empty.')
        else:
            print self.__stack[self.__top]

    def show(self):
        print self.__stack

if __name__ == '__main__':
    s = Stack(5)
    #测试入栈
    [s.push(i) for i in xrange(5)]
    s.show()
    #测试出栈
    s.pop()
    s.show()
    #测试获取栈顶元素
    s.top()
    
