# coding:utf-8
# stack.py
class Stack:
    def __init__(self, items_list = []):
        self.items = []
        # print items_list
        if len(items_list) > 0:
            self.items.extend(items_list)

    def push(self, item):
        """push item into the stack"""
        self.items.append(item)

    def pop(self):
        """pop the top item of the stack"""
        # if self.is_empty() == False:
        if not self.is_empty():
            poped_item = self.items.pop()
            return poped_item

    def is_empty(self):
        if len(self.items) > 0:
            return False
        else:
            return True

    def top(self):
        """get the top item of the stack"""
        if len(self.items) > 0:
            return self.items[-1]

    def size(self):
        return len(self.items)

def main():
    s1 = Stack()
    s1.push([12,23])
    print s1.top()

    s = Stack([1,2,3,4])
    print "size:", s.size()
    s.push({"name": "kk"})

    print "size:", s.size()
    print s.top()

    while not s.is_empty():
        print s.pop()

    print s.pop()

    print "size:", s.size()

if __name__ == "__main__":
    main()