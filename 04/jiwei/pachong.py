import re
import time
import requests
from wrapper import *

url = 'http://bbs.hupu.com/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'}
u = re.compile(r'href="(http.*?)"')
r = requests.get(url, headers=headers)
matches = re.findall(u, r.text)
matches = [ (url, 0) for url in matches ]
geted_url = set()

@timeout(1)
def myrequests(url,headers):
    r = requests.get(url, headers=headers, allow_redirects=False)

for url, num in matches:
    try:
        if num > 2:
            break
        if (url, num) in geted_url:
            continue
        geted_url.add((url, num))
        print url, num
        myrequests(url, headers)
        for i in re.findall(u, r.text):
            matches.append((i, num+1))
    except Exception as e:
        print e
        continue
