# -*- coding: utf-8 -*-
from math import sqrt

if __name__ == '__main__':
    print [ p for p in range(2, 100) if 0 not in [ p % d for d in range(2, int(sqrt(p))+1)] ]
