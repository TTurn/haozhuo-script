# coding: utf-8
import pymysql
import random
from select_proxy import SelectProxy

class GetProxy(object):

	def __init__(self):
		self.select_proxy = SelectProxy(1)

	def get_proxy(self):
		"""
		从数据库中批量抽取代理，选取任一代理，并再次验证，最终返回有效代理
		:return: 任一有效代理
		"""
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler', charset='utf8')
		cursor = conn.cursor()
		sql = 'SELECT proxy FROM valid_proxy'
		cursor.execute(sql)
		proxies = cursor.fetchall()
		conn.commit()
		cursor.close()
		conn.close()
		db_proxies = [p[0] for p in proxies]
		random_proxy = random.sample(db_proxies, 1)[0]

		proxy = {"http": "http://" + random_proxy}

		return proxy

if __name__ == "__main__":
	proxy = GetProxy()
	result = proxy.get_proxy()
	print(result)

