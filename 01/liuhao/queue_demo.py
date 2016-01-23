#!/usr/bin/env python
# -*- coding: utf-8
# Using list to achieve queue

class Queue(object):
    def __init__(self):
        self.items = []

    def push(self, value):
        return self.items.append(value)

    def pop(self):
        return self.items.pop(0)
