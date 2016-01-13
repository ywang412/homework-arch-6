#!/usr/bin/env python
# coding: utf-8

import sys

def numGen(num):
    tmp = 2
    while tmp <= num:
        yield tmp
        tmp += 1

if len(sys.argv) != 2:
    print("use prime.py <number>")
    exit(1)

number = int(sys.argv[1])
tmp = 2 

if number < 2 :
    print("number should >= 2")
    exit(1)

for i in numGen(number):
    halfnum = i / 2
    primBool = True
    tmp = 2

    while tmp <= halfnum:
        if (i % tmp) == 0:
            primBool = False
            break
        tmp += 1
    if primBool:
        print i,

