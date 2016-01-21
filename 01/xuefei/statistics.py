#!/usr/bin/env python
#coding:utf-8

#Author:Xue Fei
#Date:2016/01/20



f = open('word.txt', 'r')
num = 0
for line in f.readlines():
    line = line.replace(',',' ')
    line = line.replace('?',' ')
    line = line.replace('!',' ')
    line = line.replace('.',' ')
    list = line.split()
    while list:
        list.pop()
        num += 1

print ("The word.txt file contains a total of %s words! ") %(num)
