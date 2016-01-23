#!/usr/bin/env python
def isprime(num):
	for i in range(2,num/2+1):
		if num % i == 0:
			return False
	return True

if __name__ == '__main__':
	print filter(isprime,range(2,1001))
