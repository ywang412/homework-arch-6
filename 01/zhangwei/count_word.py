#!/usr/bin/env python
# encoding: utf-8
import re

def count_word(text):
    res = {}
    with open(text) as f:
        all_text = f.read()
        text_conversion = re.sub('\.|,|"|:|;|\(|\)', ' ', all_text)
        text_conversion = re.sub('。|，|“|”|：|；|（|）|‘|’', ' ', text_conversion)
        for word in text_conversion.replace('\n','').split():
            if word not in res:
                res[word] = 0
            res[word] += 1
        return res

if __name__ == '__main__':
    print count_word('test.txt')
