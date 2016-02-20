#!/usr/bin/env python

import xdb
import sys

def main():
    if len(sys.argv) < 3:
        print 'usage ./write.py key value'
        sys.exit(1)
    db = xdb.DB("db.xdb")
    db.set(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
