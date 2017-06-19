import requests
import toutiao_app_hyq

url = 'http://www.toutiao.com/a6404239483256291585/'
# url = url.replace("group/", "a").replace("//", "//www.")

# print(url)
#
# proxy = {'http': 'http://42.227.124.111:8088'}
#
# headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
# 				"Accept-Encoding":"gzip, deflate, sdch",
# 				"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
# 				"Cache-Control":"max-age=0",
# 				"Connection":"keep-alive",
# 				"Host":"www.toutiao.com",
# 				"Upgrade-Insecure-Requests":"1",
# 				"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# 				}
#
# r = requests.get(url, headers=headers, timeout=10)
#
# print(r.content.decode('utf-8'))


print(url)

content = toutiao_app_hyq.download_article(url, "")
print(content)
