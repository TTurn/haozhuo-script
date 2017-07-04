# coding: utf-8

"""
filter short news
"""

import pymysql
import re
from datetime import datetime
from datetime import timedelta
from matplotlib import pyplot as plt
import numpy as np

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
	cursor = conn.cursor()

	sql = "select id, content from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	cursor.close()
	conn.close()

	id_list = [result[0] for result in results]
	contents_len = [len(result[1]) for result in results]

	return id_list, contents_len


def filter(id_list, contents_len):

	delete_id_list = []
	for i in range(len(contents_len)):
		id = id_list[i]
		length = contents_len[i]
		if length < 400:
			delete_id_list.append(id)

	return delete_id_list

def delete_news(delete_id_list):
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	for i in range(len(delete_id_list)):
		id = delete_id_list[i]
		print("正在删除第{0}篇文章".format(i+1))
		sql = "delete from toutiao_app_combine_unique_20170623 where id = %s"
		cursor.execute(sql, (id, ))
		conn.commit()

	cursor.close()
	conn.close()


if __name__ == "__main__":
	id_list, contents_len = get_samples()
	# plt.hist(contents_len, bins=100, range=(0, 500), cumulative=1)
	# plt.show()
	delete_id_list = filter(id_list, contents_len)
	delete_news(delete_id_list)