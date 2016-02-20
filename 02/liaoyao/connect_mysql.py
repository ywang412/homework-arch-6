#!/usr/bin/env python

import MySQLdb as mysql

def get_data(sql_str):
	db = mysql.connect(host='127.0.0.1',user='root',passwd='lyao36843',db='liaoyao')
	db.autocommit(True)
	cur = db.cursor()
	cur.execute(sql_str)
	data = cur.fetchall()
	return data


sql = 'select * from server'
result = get_data(sql)
print "id server memory"
for i in result:
	print i[0],i[1],i[2]