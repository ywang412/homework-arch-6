#!/usr/bin/env python
import sys

def stical(newfile):
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
	return result



if __name__ == '__main__':
	if len(sys.argv) <= 1:
		print 'Please given a parameter'
	else:
		for k in stical(sys.argv[1]):
			print "%s : %s" % (k,stical(sys.argv[1])[k])
