#!/usr/bin/env python

#coding:utf-8

#*para	表示接受一个元组
#**para	表示接受一个字典
#*para 要在**para之前

def test(*args,**dic):
	for arg in args:
		print arg
	for k,v in dic.iteritems():
		print k,":",v


test("yes",1,2,me="auxten",where="beijing")