#!/usr/bin/env python
# coding: utf-8

from StackAndQueue import Stack
from StackAndQueue import Queue

def testStack():
    myStack = Stack()

    print("test Stack.pop()")
    result = myStack.pop()
    print("empty stack pop return", type(result))

    print("push data: test string, hello")
    myStack.push("test string")
    myStack.push("hello")

    print("Stack:", myStack._Stack__list)
    print("Stack size:", myStack._Stack__size)

    result = myStack.pop()
    print("pop stack return:", result)
    print("Stack:", myStack._Stack__list)
    print("Stack size:", myStack._Stack__size)


def testQueue():
    myQueue = Queue()

    print("\ntest Queue.pop()")
    result = myQueue.pop()
    print("empty Queue pop return", type(result))

    print("push data: test string, hello")
    myQueue.push("test string")
    myQueue.push("hello")

    print("Queue:", myQueue._Queue__list)
    print("Queue size:", myQueue._Queue__size)

    result = myQueue.pop()
    print("pop Queue return:", result)
    print("Queue:", myQueue._Queue__list)
    print("Queue size:", myQueue._Queue__size)

if __name__ == '__main__':
    testStack()
    testQueue()
