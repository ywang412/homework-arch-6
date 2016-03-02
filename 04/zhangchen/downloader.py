#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import urllib2
import threading

def print_usg():
    pass

def check_argv():
    if len(sys.argv) != 3:
        print_usg()
    elif not sys.argv[1].startswith('http://')
        print_usg()
    try:
        num = int(sys.argv[2])
    except ValueError,e:
        print_usg()
    return (sys.argv[1],num)

