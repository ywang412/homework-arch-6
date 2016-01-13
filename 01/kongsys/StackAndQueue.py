#!/usr/bin/env python
# coding: utf-8

class Stack:

    def __init__(self, *base):
        self._list = list(base)
        self._size = len(self._list)

    def push(self, elem):
        self._list.append(elem)
        self._size += 1

    def pop(self):
        if self._size < 1:
            return None
        else:
            elem = self._list[-1]
            del self._list[-1]
            self._size -= 1
            return elem


class Queue:
    
    def __init__(self, *base):
        self._list = list(base)
        self._size = len(self._list)

    def push(self, elem):
        self._list.append(elem)
        self._size += 1

    def pop():
        if self._size < 1:
            return None
        else:
            elem = self._list[0]
            del self._list[0]
            self._list -= 1
            return elem
