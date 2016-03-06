import threading
import time

class Person:
    def __init__(self):
        self.money = 100
        self.lock = threading.Lock()

    def borrow(self, p, n):
        if self.money >= n:
            p.money += n
            time.sleep(3)
            self.money = self.money - n
            print 'borrow %d money, %d left' %(n, self.money)
        else:
            print "money not enougth", self.money

    def total(self):
        return self.money

p1 = Person()
p2 = Person()


def run(p1, p2, n):
    p1.borrow(p2, n)

if __name__ == '__main__':
    p1 = Person()
    p2 = Person()
    t1 = threading.Thread(target=run, args=(p1, p2, 10))
    t2 = threading.Thread(target=run, args=(p1, p2, 100))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print p1.total()
