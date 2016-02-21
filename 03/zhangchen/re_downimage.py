#!/usr/bin/env python
#coding=utf-8

import urllib2
import re

url = 'http://www.douban.com/people/ahbei/'
headers = {'User-Agent':'ss'}
req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)
the_page = response.read()

p = re.compile(ur'<img src="(.*?)"\sclass="m_sub_img"')
matches = re.findall(p, the_page)
print matches 
for m in matches:
    with file(m.split("/")[-1],"w") as f:
        f.write(urllib2.urlopen(m).read())
