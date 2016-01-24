# coding:utf-8
# queue.py

class Queue():
    def __init__(self, queue_list = []):
        self.items = []
        if len(queue_list) > 0:
            self.items.extend(queue_list)

    def size(self):
        """return the size of queue"""
        return len(self.items)

    def is_empty(self):
        """return whether the queue is empty"""
        if self.size() == 0:
            return True
        else:
            return False

    def pop(self):
        """pop the front item of the queue"""
        if not self.is_empty():
            return self.items.pop(0)

    def push(self, pushed_items):
        self.items.append(pushed_items)

    def front(self):
        """get the front item of the queue"""
        if not self.is_empty():
            return self.items[0]

def main():
    q1 = Queue()
    print q1.pop()
    for i in range(5):
        q1.push(i)

    print "front: ", q1.front()
    print "queue size: ", q1.size()

    for i in range(6):
        print "poped: ", q1.pop()
        print "queue size: ", q1.size()



if __name__ == "__main__":
    main()