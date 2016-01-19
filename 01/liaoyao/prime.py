#!/usr/bin/env python

def isprime(number):
	for i in range(2,number/2+1):
		if number % i == 0:
			return False
	return True

if __name__ == '__main__':
	print filter(isprime,range(2,1001))
