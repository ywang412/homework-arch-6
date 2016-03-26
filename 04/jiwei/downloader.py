#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    elif not sys.argv[1].startswith('http://'):
        print_usg()
    try:
        num = int(sys.argv[2])
    except:
        print_usg()
    return (sys.argv[1], num)

class downloader(object):
    def __init__(self, p_url, p_num):
        self.url, self.num = (p_url, p_num)
        self.name = self.url.split('/')[-1]
        self.total = int(requests.head(self.url).headers['Content-Length'])
        self.offset = int(self.total / self.num) + 1
        print '\ninit:\n\tfile size: %d, offset: %d' %(self.total, self.offset)

    def gen_ranges(self):
        ranges = []
        for i in xrange(self.num):
            j = i * self.offset
            if (j + self.offset) > self.total:
                ranges.append((j, self.total))
            else:
                ranges.append((j, j+self.offset))
        return (ranges)

    def save_range(self, p_cont, p_from):
        try:
            fd = os.dup(self.fd.fileno())
            fd_wr = os.fdopen(fd, 'w+')
            fd_wr.seek(p_form)
            fd_wr.write(p_cont)
            fd_wr.close()
        except Exception as e:
            print e.strerror

    def thread_handler(self, p_start, p_end):
        try:
            r = requests.get(self.url,headers={'Range':'Bytes='+str(p_start)+'-'+str(p_end)})
        except:
            print 'error when open url: %s' %self.url
            sys.exit(2)
        self.save_range(r.text, p.start)

    def run(self):
        self.fd = open(self.name, 'w+')
        thread_list = []
        n = 0
        for item_range in self.gen_ranges():
            start, end = item_range
            print 'thread %d - start: %s, end: %s' %(n, start, end)
            thread = threading.Thread(target=self.thread_handler, args=(start, end))
            thread.start()
            thread_list.append(thread)
            n += 1

        for i in thread_list:
            i.join()

        self.fd.close()
        print 'file: %s download success!' %self.name

if __name__ == '__main__':
    url ,num = check_argv()
    down = downloader(url, num)
    down.run()

