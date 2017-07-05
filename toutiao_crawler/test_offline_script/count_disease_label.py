# coding: utf-8
"""
判断文章中含有疾病标签的篇数
"""

import pymysql

def get_disease_label():
	with open("disease_label_hjb", 'r') as f:
		lines = f.readlines()
		disease_labels = [line.strip() for line in lines]

	return disease_labels

def get_content():
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select content from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章-------".format(len(results)))


	contents = [result[0] for result in results]

	cursor.close()
	conn.close()

	return contents

def judge_single(disease_labels, content):

	for label in disease_labels:
		if label in content:
			return True

	return False

def count(disease_labels, contents):
	good_sample = 0
	bad_sample = 0

	for i in range(len(contents)):
		print("正在判断第{0}篇文章".format(i+1))
		content = contents[i]
		if judge_single(disease_labels, content):
			good_sample += 1
		else:
			bad_sample += 1
	print(good_sample)
	print(bad_sample)

if __name__ == "__main__":
	disease_labels = get_disease_label()
	contents = get_content()
	count(disease_labels, contents)