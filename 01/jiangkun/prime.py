# coding:utf-8
import math

# prime version 1
# 返回N以内的素数，N > 0
# 筛法
def prime(n):
    prime_list = []
    if n == 2:
        prime_list.append(2)
    elif n == 3:
        prime_list.extend([2, 3])
    elif n > 3:
        num_list = [ x>=2 for x in xrange(n+1)]
        # print num_list
        # 偶数是非质数 -- False
        for i in xrange(4, n+1):
            if i % 2 == 0:
                num_list[i] = False
        # print num_list
        # (n+1)/2  --优化-- sqrt(n+1)
        bond = int(math.ceil(math.sqrt(n+1))) + 1
        # print bond
        # return
        for i in xrange(3, bond):
            # 筛掉1-n中最小的质数的倍数，下一个True的是质数
            # 是偶数或者质数的倍数, continue
            # print "*" * 20
            # print i
            if num_list[i] == False:
                continue

            # 筛掉质数的倍数
            for j in xrange(i+1, n+1):
                if j % i == 0:
                    num_list[j] = False
            # print num_list

        for i in xrange(n+1):
            if num_list[i]:
                prime_list.append(i)
    
    return prime_list


def main():
    for i in range(15):
        print i, prime(i)
    # print prime(15)
    print prime(1000000)

if __name__ == "__main__":
    main()