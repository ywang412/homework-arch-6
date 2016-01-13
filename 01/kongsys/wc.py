#!/usr/bin/env python
# coding: utf-8

#A ~ Z ascii value 65 ~ 90
#a ~ z ascii value 97 ~ 122
#0 ~ 9 ascii value 48 ~ 57
apostrophe = 39 # ' ascii value
fileob = open("testdata.txt")
str = ''
wordDict = {}

def isLetOrNum(value):
    if (value >= 65) and (value <= 90):
        return True

    if (value >= 97) and (value <= 122):
        return True

    if (value >= 48) and (value <= 57):
        return True

    return False


def addWordDict(word):
    if word in wordDict.keys():
        wordDict[word] += 1
    else:
        wordDict[word] = 1


while True:
    letter = fileob.read(1)
    if len(letter) == 0:
        break
    
    if isLetOrNum(ord(letter)):
        str += letter
        continue
    if ord(letter) == apostrophe:
        temp = fileob.read(1)
        if len(temp) == 0:
            addWordDict(str)
            break

        if isLetOrNum(ord(temp)):
            str += letter +temp
            continue

    if len(str) > 0:
        addWordDict(str)
        str = ''

for i in wordDict:
    print i, wordDict[i]
