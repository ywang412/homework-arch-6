import os
import sys
import requests
import threading

def print_usg():
    print 'usage:\n\t' + sys.argv[0] + ' http://URL THREAD_NUM'
    sys.exit(1)

def check_argv():
    if len(sys.argv) != 3:
        print_usg()
    elif not sys.argv[1].startswitch('http://'):
        print_usg()
    try:
        num = int(sys.atgv[2])
    except:
        print_usg()
    return (sys.argv[1], num)
