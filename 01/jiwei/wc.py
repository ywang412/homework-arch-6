# -*- coding: utf-8 -*-
import sys
import re

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        print len(re.findall('\w+', f.read(1024*1024)))
