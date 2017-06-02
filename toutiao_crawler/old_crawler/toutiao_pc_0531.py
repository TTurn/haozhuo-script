# coding: utf-8

import requests

headers = {'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6', 'Accept-Encoding': 'gzip, deflate, sdch, br', 'Host': 'www.toutiao.com', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Upgrade-Insecure-Requests': '1', 'Connection': 'keep-alive', 'Cookie': 'uuid="w', 'Cache-Control': 'max-age=0', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
url = "https://www.toutiao.com/ch/news_health/"

r = requests.get(url, headers=headers)
print(r.content)