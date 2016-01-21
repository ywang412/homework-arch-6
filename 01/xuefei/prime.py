#!/usr/bin/env python
#coding:utf-8

#Author:Xue Fei
#Date:2016/01/18


from math import sqrt

def prime(self):
    list = [p for p in range(2,self) if 0 not in [p % d for d in range(2,int(sqrt(p)) + 1)]]
    print list

def is_num_by_except(num):
    try:
        int(n)
        return True
    except ValueError:
        print("您输入的 \"%s\" 不是数字, 请重新执行!") %(n)


if __name__ == '__main__':
    n = raw_input("请输入您想输出的质数范围: ")
    if is_num_by_except(n) is True:
         num = int(n)
         prime(num)

