# coding: utf-8
"""
增加原生的类别、标签
"""

import pymysql
import toutiao_app_hyq
from bs4 import BeautifulSoup
import multiprocessing
from get_proxy import GetProxy


def get_url():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select id, display_url from toutiao_app_combine_unique_20170616 where raw_class = ''"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章-------".format(len(results)))


	ids = [result[0] for result in results]
	urls = [result[1] for result in results]

	cursor.close()
	conn.close()

	return ids, urls

def get_label_class(url, proxies):
	content = toutiao_app_hyq.download_article(url, proxies)
	soup = BeautifulSoup(content, 'lxml')
	# try:
	news_class = soup.find_all(ga_event="click_channel")[0].get_text()
	# except:
	# 	news_class = ""
	# try:
	news_label_list = ",".join(soup.find_all(class_="label-list")[0].get_text().split())
	# except:
	# news_label_list = ""

	return news_class, news_label_list

def save_label_class(id, news_class, news_label_list):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "UPDATE toutiao_app_combine_unique_20170616 SET raw_class = %s, raw_label = %s WHERE id = %s"
	cursor.execute(sql, (news_class, news_label_list, id))
	conn.commit()
	cursor.close()
	conn.close()

def engine_single(ids, urls, i, proxies):
	id = ids[i]
	url = urls[i].replace("group/", "a").replace("//", "//www.")
	print("--正在转换存储第{0}篇文章  {1}".format(i+1, id))
	try:
		news_class, news_label_list = get_label_class(url, proxies)
		save_label_class(id, news_class, news_label_list)
	except:
		print("文章无法存储转换  {0}".format(id))


def engine():
	ids, urls = get_url()
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	# proxy = GetProxy()
	proxies = ""
	# proxies = {'http': 'http://42.227.124.111:8088'}

	for i in range(len(ids)):
		# proxies = proxy.get_proxy()
		# engine_single(ids, urls, i, proxies)
		pool.apply_async(engine_single, (ids, urls, i, proxies))

	pool.close()
	pool.join()

if __name__ == "__main__":
	# test
	# id = 9987
	# url = "http://www.toutiao.com/a135308687/"
	# news_class, news_label_list = get_label_class(url)
	# print(news_class, news_label_list)
	# save_label_class(id, news_class, news_label_list)

	# run

	engine()