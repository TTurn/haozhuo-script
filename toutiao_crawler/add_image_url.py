# coding: utf-8
"""
增加image_url，这个字段，抽取每个html里面的第一个图片src
作为缩略图，列表图使用
"""

import pymysql
from bs4 import BeautifulSoup

def get_id_html():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select id, htmls from toutiao_app_combine_unique_20170620"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章-------".format(len(results)))

	ids = [result[0] for result in results]
	htmls = [result[1] for result in results]

	cursor.close()
	conn.close()

	return ids, htmls

def extract_image(html):
	soup = BeautifulSoup(html, 'lxml')
	image_list = []
	for _ in soup.find_all('img'):
		image_list.append(_['src'])

	return image_list

def save_image(ids, htmls):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	for i in range(len(ids)):
		print("----正在存储第{0}篇文章-----".format(i+1))
		id = ids[i]
		html = htmls[i]
		image_list = extract_image(html)
		sql = "UPDATE toutiao_app_combine_unique_20170620 SET image_thumbnail = %s, image_list = %s WHERE id = %s"
		image_thumbnail = image_list[0] if image_list else ""
		image_list = ",".join(image_list) if image_list else ""
		cursor.execute(sql, (image_thumbnail, image_list, id))
		conn.commit()

	cursor.close()
	conn.close()




if __name__ == "__main__":
	ids, htmls = get_id_html()
	save_image(ids, htmls)