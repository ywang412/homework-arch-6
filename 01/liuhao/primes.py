#!/usr/bin/env python
# -*- coding: utf-8
# calculation prime number

def primes(number):
    """
    calculation prime number
    :param key: number
    :return: a list of prime numbers from 2 to < n
    """
    if number < 2:
        return []
    if number == 2:
        return [2]
    odd = range(3, number, 2)
    square_root = number ** 0.5
    half = len(odd)
    location = 0
    prime_number = 3
    while prime_number <= square_root:
        if odd[location]:
            un_prime_number_location = (prime_number ** 2 - 3)//2
            odd[un_prime_number_location] = 0
            while un_prime_number_location < half:
                odd[un_prime_number_location] = 0
                un_prime_number_location += prime_number
        location = location + 1
        prime_number = 2 * location + 3
    return [2] + [number for number in odd if number]


def main():
    primes(2000000)

if __name__ == '__main__':
    main()

