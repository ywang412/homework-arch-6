# -*- coding: utf-8 -*-
import time
from math import sqrt, ceil

def get_prime(n):
    candicates = [True] * (n + 1)
    candicates[0] = candicates[1] = False
    # 求平方根并往上取整，求n/2的质数
    for i in xrange(2, int(ceil(sqrt(n)))): 
        # 已被筛除的整数，跳过
        if not candicates[i]:  
            continue
        # 筛除质数的倍数
        for j in xrange(i*i, n+1, i):
            candicates[j] = False
    return [i for i in xrange(n+1) if candicates[i]]

if __name__ == '__main__':
    num = 100000000
    start = time.time()
    total = get_prime(num)
    end = time.time()
    print 'The prime numbers from 1 to %s is %s' %(num, len(total))
    print 'Time spent: %s' %(end-start)
