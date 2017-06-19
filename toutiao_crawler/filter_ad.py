# coding: utf-8

"""
过滤包含购买链接的资讯
"""

import re
from bs4 import BeautifulSoup
import pymysql
import multiprocessing

def get_ids():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select id, content, htmls from toutiao_app_combine_unique_20170616 where content like '%pgc-card .pgc-card-href%'"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章有广告链接-------".format(len(results)))


	ids = [result[0] for result in results]
	contents = [result[1] for result in results]
	htmls = [result[2] for result in results]

	cursor.close()
	conn.close()

	return ids, contents, htmls

def save_content_html(id, content, html):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "UPDATE toutiao_app_combine_unique_20170616 SET content = %s, htmls = %s WHERE id = %s"
	cursor.execute(sql, (content, html, id))
	conn.commit()
	cursor.close()
	conn.close()



def sub_ad_content(content):
	content_clean = re.sub("#pgc(.*?)购买", "", content, flags=re.S)

	return content_clean

def sub_ad_html(html):
	soup = BeautifulSoup(html, 'lxml')
	for _ in soup.find_all("style"):
		_.decompose()
	for _ in soup.find_all(class_=re.compile("pgc.*")):
		_.decompose()

	return soup

def engine_single(i, ids, contents, htmls):
	id = ids[i]
	print("--正在转换存储第{0}篇文章  {1}".format(i + 1, id))
	content = contents[i]
	html = htmls[i]
	content_clean = sub_ad_content(content)
	html_clean = sub_ad_html(html)
	save_content_html(id, content_clean, html_clean)

def engine():
	ids, contents, htmls = get_ids()
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	for i in range(len(ids)):
		engine_single(i, ids, contents, htmls)
		# pool.apply_async(engine_single, (i, ids, contents, htmls))

	pool.close()
	pool.join()


if __name__ == "__main__":
	# with open("ad_html.txt", 'r') as f:
	# 	html = f.read()
	# sub_ad_html(html)

	# select count(*) from toutiao_app_combine_unique_20170616 where htmls like "%pgc-card .pgc-card-href%"

	engine()
