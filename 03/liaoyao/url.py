#!/usr/bin/env python
#coding=utf-8

import urllib2
import re




def gethtml(url):
	headers = {'User-Agent':'ss'}
	req = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(req)
	return response.read()	


def getimg(html):
	match = re.compile(r'<img src="(.*?)"\sclass="m_sub_img"')
	matches = re.findall(match,html)
	for m in matches:
		with file(m.split("/")[-1],"w") as f:
			f.write(gethtml(m))

if __name__ == "__main__":
	url = 'http://www.douban.com/people/ahbei/'
	getimg(gethtml(url))
