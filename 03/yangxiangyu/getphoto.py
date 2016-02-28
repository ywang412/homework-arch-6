#!/usr/bin/env python
# encoding: utf-8

import urllib
import re

result = urllib.urlopen("http://www.douban.com/people/ahbei/")
html = result.read()
pattern = re.compile(r'http://([^"]+jpg)')
photo = re.findall(pattern, html)
print(photo)
for url in photo:
    filename = url.split('/')[-1]
    url = "http://"+ url
    urllib.urlretrieve(url, filename)
