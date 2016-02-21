import re
import requests

url = 'http://www.douban.com/people/anbei/'
r = requests.get(url, headers={'User-Agent':'jiwei'})
p = re.compile(ur'<img src="(.*?)"\sclass="m_sub_img"')
matches = re.findall(p, r.text)
print matches
for m in matches:
    with open(m.split("/")[-1], 'w') as f:
        f.write(requests.get(m).content)
