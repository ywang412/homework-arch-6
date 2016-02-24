#!/usr/bin/env python
#coding=utf-8

import urllib2
import re


class GetImg():

	def gethtml(self,url):
		headers = {"User-Agent":"ss"}
		req = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(req)
		return response.read()

	def gethref(self,html,count=None):			#截取http://www.douban.com/people/xxxxx,使用dict更合适
		href_list = []
		match_str = re.compile(r'<a href=".*"\sclass="nbg".*</a>')
		match = re.findall(match_str,html)
		for line in match:
			href = line.split()[1].split('"')[1]
			href_list.append(href)
		return href_list
		

if __name__ == "__main__":
	url = 'http://www.douban.com/people/ahbei/'
	con = GetImg()
	html = con.gethtml(url)
	href_list = con.gethref(html)   
	print href_list

	#for href in href_list:
	#	print href	
	#	print "lllll"
	#print href_list