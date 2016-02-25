#!/usr/bin/env python
#coding=utf-8

import urllib2
import re


class GetImg():
	def __init__(self):
		self.href = {}
		self.img = {}

	def gethtml(self,url):
		headers = {"User-Agent":"ss"}
		req = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(req)
		return response.read()

	"""def gethref(self,html,count=None):			#截取http://www.douban.com/people/xxxxx,使用dict更合适
		href_list = []
		match_str = re.compile(r'<a href=".*"\sclass="nbg".*</a>')
		match = re.findall(match_str,html)
		for line in match:
			href = line.split()[1].split('"')[1]
			href_list.append(href)
		return href_list"""
	
	def imgurl(self,html):
		img_str = re.compile('<img src="(.*?)"\sclass="m_sub_img"')
		match_img = re.findall(img_str,html)
		for img in match_img:
			self.img[img] = 1

	def gethref(self,html,count=None):			#截取http://www.douban.com/people/xxxxx,使用dict更合适
		self.imgurl(html)
		match_str = re.compile(r'<a href=".*"\sclass="nbg".*</a>')
		match = re.findall(match_str,html)
		while count > 1:
			for line in match:
				href = line.split()[1].split('"')[1]
				tmp = self.gethtml(href)
				self.gethref(tmp)
			count -= 1 
		return self.img


if __name__ == "__main__":
	url = 'http://www.douban.com/people/ahbei/'
	con = GetImg()
	html = con.gethtml(url)
	img_dict = con.gethref(html,5)   
	for k,v in img_dict.items():
		img_name = k.split('/')[-1]
		with file(img_name,'w') as f:
			f.write(con.gethtml(k))	




