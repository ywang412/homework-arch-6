#!/usr/bin/env python
# encoding: utf-8

import math


def is_prime(x):
    for i in range(2, int(math.sqrt(x))):
        if x % i == 0:
            return False
    return x


def prime(n):
    r = filter(is_prime, range(2, n))
    return list(r)

print(prime(100000))
