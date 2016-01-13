#!/usr/bin/env python
import sys

def wcount(file):
    wnum={}
    f=open(file,'r')
    for line in f.readline():
        for word in line.split():
            if word in wnum:
                wnum[word]=wnum[word]+1
            else:
                wnum[word]=1
    return wnum





if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print 'please give me a file name'
    for key,v in wcount(sys.argv[1]).items():
       print key,v
