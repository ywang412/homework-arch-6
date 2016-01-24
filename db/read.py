#!/usr/bin/env python

import xdb
import sys

def main():
    if len(sys.argv) < 2:
        print 'usage ./read.py key'
        sys.exit(1)
    db = xdb.DB("db.xdb")
    for k in sys.argv[1:]:
        print db.get(k)

if __name__ == '__main__':
    main()
