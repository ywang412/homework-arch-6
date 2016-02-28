#!/bin/env python
#coding:utf8

import urllib2
import urllib
import re

__author__ = 'zhangchen'

class Crawler(object):
    def __init__(self,url):
        self.url = url
        self.set_url = [] #去重后url列表
        self.tmp_url = [] #临时url列表

    def _req_url(self,url): #打开每个连接的页面
        headers = {'User-Agent':'ss'}
        req = urllib2.Request(self.url, headers=headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.reason
        else:
            print 'ok'
        the_page = response.read()
        return the_page

    def _one_page(self): #打开首页
        return self._req_url(self.url)

    def depth_open_url(self,the_page=None): #获取每个页面的a标签连接
        if the_page == None:
            the_page = self._one_page()
        p = re.compile(ur'<a.*href="(https.+?)"/*?>.*?<\/a>')
        matches = p.findall(the_page)
        if matches:
            return matches
        else:
            return []

    def max_depth(self,matches,depth):
        self.set_url = matches
        if depth > 0:
            for per_page_url in matches:
                tmp_page = self._req_url(per_page_url)
                tmp_pageurl_list = self.depth_open_url(tmp_page)
                self.tmp_url += tmp_pageurl_list
            return matches+self.max_depth(self.tmp_url,depth-1)
        else:
            return matches


    def mass_remove(self,matches):
        return list(set(matches))

if __name__ == '__main__':
    test=Crawler('http://www.douban.com/people/ahbei/')
    tmp=test.depth_open_url()
    print test.max_depth(tmp,1)
