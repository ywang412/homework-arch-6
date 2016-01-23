class Stack:
    def __init__(self):
        self.items = []

    def push(self, elem):
        return self.items.append(elem)

    def pop(self):
        return self.items.pop()


class Queue:
    def __init__(self):
        self.items = []

    def push(self, elem):
        return self.items.append(elem)

    def pop(self):
        return self.items.pop(0)
