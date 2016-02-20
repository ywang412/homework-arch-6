import re


def head_none(s):
    if re.match(r'\s', s[0]):
        return True
    return False


def tail_none(s):
    if re.match(r'\s', s[-1]):
        return True
    return False


def count_word(s, tail_none, head_none):
    count = len(re.findall(r'\b\w+\b', s))
    if not tail_none and not head_none:
        return count - 1
    else:
        return count

with open('bigfile', 'r') as f:
    sum = 0
    head_blank = True
    tail_blank = True
    while True:
        result_data = f.read(10)
        if not result_data:
            break
        head_blank = head_none(result_data)
        sum = count_word(result_data, head_blank, tail_blank) + sum
        tail_blank = tail_none(result_data)
    print(sum)
