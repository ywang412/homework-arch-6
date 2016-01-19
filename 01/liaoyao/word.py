#!/usr/bin/env python
import sys

def statistical(newfile):
	f = open(newfile)
	result = {}
	while True:
		if f.readline():
			for world in f.readline().split():
				if world in result:
					result[world] += 1
				else:
					result[world] = 1
		else:
			break
	f.close()
	for k in result:
		print "%s : %s" % (k,result[k])



if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Please given a parameter'
	else:
		statistical(sys.argv[1])
