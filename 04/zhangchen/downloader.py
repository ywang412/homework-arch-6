#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import urllib2
import threading

def print_usg():
    print 'usage:\n\t{argv0} http://URL THREAD_NUM'.format(argv0=sys.argv[0])

def check_argv():
    if len(sys.argv) != 3:
        print_usg()
    elif not sys.argv[1].startswith('http://'):
        print_usg()
    try:
        num = int(sys.argv[2])
    except ValueError,e:
        print_usg()
    return (sys.argv[1],num)

class downloader(object):
    def __init__(self,p_url,p_num):
        self.url,self.num = (p_url,int(p_num))
        self.name = self.url.split('/')[-1]
        req = urllib2.Request(self.url)
        req.get_method = lambda:'HEAD' #改变请求方法为HEAD
        resp = urllib2.urlopen(req).headers
        self.total = int(resp['Content-Length'])
        self.offset = int(self.total/self.num) + 1 #计算每个线程下载偏移量
        print '\ninit:\n\tfile size:{stotal},offset:{snum}'.format(stotal=self.total,snum=self.offset)

    def gen_ranges(self):
        thread_ranges = []
        for i in xrange(self.num)
            j = i * self.offset
            if (j + self.offset) > self.total: #如果超出范围，则取文件总大小值
                thread_ranges.append((j,self.total))
            else:
                thread_ranges.append((j,j + self.offset))
        return thread_ranges

    def save_range(self,p_count,p_from):
        try:
            fd = os.dup(self.fd.fileno())
            fd_wr = os.fdopen(fd,'w+')
            fd_wr.seek(p_from)
            fd_wr.write(p_count)
            fd_wr.close()
        except Exception as e:
            print e.strerror

    def thread_handler(self,p_start,p_end):
        req = urllib2.Request(self.url)
        req.add_header('Range','Bytes=' + str(p_start) + '-' + str(p_end))
        try:
            resp = urllib2.urlopen(req)
        except:
            print 'error when open url:{error_url}'.format(error_url = self.url)
            sys.exit(2)
        self.save_range(resp.read(),p_start)

    def run(self):
        self.fd = open(self.name,'w+')
        thread_list = []
        n = 0
        for item_range in self.gen_ranges():
            start, end = item_range
            print 'thread {n} - start: {start},end: {end}'.format(n=n,start=start,end=end)
            thread = threading.Thread(target=self.thread_handler,args=(start,end))
            thread.start()
            thread_list.append(thread)
            n += 1
        for i in thread_list:
            i.join()


if __name__ == '__main__':
    check_argv()
    downloader(sys.argv[1],sys.argv[2])
