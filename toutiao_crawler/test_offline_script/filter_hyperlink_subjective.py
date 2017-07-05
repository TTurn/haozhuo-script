#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/22 15:30
# @Author  : Tuhailong
# @Site    : 
# @File    : url_me_filter.py
# @Software: PyCharm Community Edition

import pymysql
import re
from bs4 import BeautifulSoup

def get_sample():
	print("获取样本")
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag',passwd='yjkdatag',db='news_crawler',charset='utf8')
	cursor = conn.cursor()

	sql = "select id from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()
	length = len(cursor.fetchall())
	print("一共有{0}个样本".format(length))

	sql = "select id, htmls from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	id_list = [result[0] for result in results]
	content_list = [BeautifulSoup(result[1], 'lxml').get_text() for result in results]
	html_list = [result[1] for result in results]


	cursor.close()
	conn.close()

	return id_list, content_list, html_list

def me_filter(id_list,content_list):
	pattern1 = re.compile('我们')
	pattern2 = re.compile('我')

	del_me_id_list = []

	for i in range(len(id_list)):
		id = id_list[i]
		content = content_list[i]

		match1 = pattern1.findall(content)
		num_we = len(match1)
		match2 = pattern2.findall(content)
		num_me = len(match2)

		if num_me - num_we >= 12:
			del_me_id_list.append(id)

	return del_me_id_list

def delete_news(id_list):
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	for id in id_list:
		sql = "delete from toutiao_app_combine_unique_20170623 where id = %s"
		cursor.execute(sql, (id,))
	conn.commit()
	cursor.close()
	conn.close()

def url_filter(id_list, content_list):
	# url识别的正则表达式
	pattern = re.compile('[\(|（|\[|①|②|③|：]?(https|http|www){1}(:|\.|[a-z]|\d|_|[A-Z]|/| |\?|%|=|&|#|;)+[\)|）|\]|］]?')
	revise_link_id_list = []
	revise_link_loc_list = []
	revise_link_spec_list = []

	for i in range(len(id_list)):
		id = id_list[i]
		content = content_list[i]

		match = re.search(pattern, content)
		if match:
			spec = match.group()
			revise_link_id_list.append(id)
			revise_link_loc_list.append(i)
			revise_link_spec_list.append(spec)

	return revise_link_id_list, revise_link_loc_list, revise_link_spec_list

def sub_html(html, spec):
	html_clean = html.replace(spec, "")

	return html_clean

def revise_news(revise_link_id_list, revise_link_loc_list, revise_link_spec_list, html_list):
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	for i in range(len(revise_link_id_list)):
		id = revise_link_id_list[i]
		print("正在修正第{0}篇文章  {1}".format(i+1, id))
		loc = revise_link_loc_list[i]
		html = html_list[loc]
		spec = revise_link_spec_list[i]
		html_clean = sub_html(html, spec)

		sql = "update toutiao_app_combine_unique_20170623 set htmls = %s where id = %s"
		cursor.execute(sql, (html_clean, id))
		conn.commit()

	cursor.close()
	conn.close()

if __name__ == "__main__":
	id_list, content_list, html_list = get_sample()
	del_me_id_list = me_filter(id_list, content_list)
	print("包含“我”的文章：{0}".format(del_me_id_list))
	print("长度：{0}".format(len(del_me_id_list)))
	delete_news(del_me_id_list)

	revise_link_id_list, revise_link_loc_list, revise_link_spec_list = url_filter(id_list, content_list)
	print("包含链接的文章：{0}".format(revise_link_id_list))
	print("长度：{0}".format(len(revise_link_id_list)))

	revise_news(revise_link_id_list, revise_link_loc_list, revise_link_spec_list, html_list)

	for i in range(len(revise_link_id_list)):
		id = revise_link_id_list[i]
		spec = revise_link_spec_list[i]
		print(str(id)+"-------------"+spec)
