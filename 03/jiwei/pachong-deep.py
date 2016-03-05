import re
import requests

cookie = 'q_c1=908a190222294811aa95bc45d4b90d40|1456293207000|1456293207000; _xsrf=3d2957bff09dc0a6f2a67012e353897e; _za=f49ce95a-1499-4ade-9e20-d4e49abb83db; td_cookie=1850149171; __utmt=1; cap_id="NGQ5ODlkY2RkMWQ1NGY4NWJiZjIxM2U2N2IwOGU0M2U=|1456474929|456c6f0b9def97daf0151b977d7b8fabed7a0fb8"; z_c0="QUFEQW5ZWWFBQUFYQUFBQVlRSlZUWkdZOTFhOGQ1THhwSVNfdU5rN29vcXI5Y0JpQkVOdGd3PT0=|1456475025|f19402328bc458b08dbc464ae2ece81b13ceaa15"; unlock_ticket="QUFEQW5ZWWFBQUFYQUFBQVlRSlZUWmtTMEZZZVJXUkN4OHk2ZWh6X0ZCdExuRFJGUnplWXZRPT0=|1456475025|c5f0178fbb41124234c29a4dd48bbf599f919d7b"; n_c=1; __utma=51854390.920822231.1456293145.1456293145.1456474851.2; __utmb=51854390.10.10.1456474851; __utmc=51854390; __utmz=51854390.1456293145.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20130320=1^3=entry_date=20130320=1'
headers = {'cookie': cookie}
r = requests.get('https://www.zhihu.com/people/ji-wei-65', headers=headers)
geted_url = {}
urls = re.findall('[htps]+://[^\s"&]*', r.text)

for i in urls:
    r = requests.get(i, headers=headers)
    print i,r.text
    geted_url[i] = r.text
print len(geted_url)
