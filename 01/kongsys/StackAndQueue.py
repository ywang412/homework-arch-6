#!/usr/bin/env python
# coding: utf-8

class Stack:

    def __init__(self, *base):
        self.__list = list(base)
        self.__size = len(self.__list)

    def push(self, elem):
        self.__list.append(elem)
        self.__size += 1

    def pop(self):
        if self.__size < 1:
            return None
        else:
            elem = self.__list[-1]
            del self.__list[-1]
            self.__size -= 1
            return elem


class Queue:
    
    def __init__(self, *base):
        self.__list = list(base)
        self.__size = len(self.__list)

    def push(self, elem):
        self.__list.append(elem)
        self.__size += 1

    def pop(self):
        if self.__size < 1:
            return None
        else:
            elem = self.__list[0]
            del self.__list[0]
            self.__size -= 1
            return elem
