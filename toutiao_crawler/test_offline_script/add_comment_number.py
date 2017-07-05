# coding: utf-8
"""
增加原生资讯的评论数
"""

import toutiao_app_hyq
from bs4 import BeautifulSoup
import re
import pymysql
import multiprocessing

def get_url():
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select id, display_url from toutiao_app_combine_unique_20170623 where comment_count is NULL"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章-------".format(len(results)))


	ids = [result[0] for result in results]
	urls = [result[1] for result in results]

	cursor.close()
	conn.close()

	return ids, urls

def get_comment_count(url):
	content = toutiao_app_hyq.download_article(url, "")
	soup = BeautifulSoup(content, 'lxml')
	for tag in soup.find_all("script"):
		pattern = re.compile("\d+")
		if "utils.numCutByComma" in tag.get_text():
			line = tag.get_text().split("\n")[4]
			comment_count = re.search(pattern, line).group()

	return comment_count

def save_comment_count(id, count):
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "UPDATE toutiao_app_combine_unique_20170623 SET comment_count = %s WHERE id = %s"
	cursor.execute(sql, (count, id))
	conn.commit()
	cursor.close()
	conn.close()

def engine_single(id, url, i):
	print("存储第{0}篇文章  {1}".format(i + 1, id))
	try:
		comment_count = get_comment_count(url)
		save_comment_count(id, comment_count)
	except:
		print("--------{0}----------没有评论界面".format(url))

def engine():
	ids, urls = get_url()
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	for i in range(len(ids)):
		id = ids[i]
		url = urls[i]
		engine_single(id, url, i)
		# pool.apply_async(engine_single, (id, url, i))

	pool.close()
	pool.join()


if __name__ == "__main__":
	engine()