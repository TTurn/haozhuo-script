# coding: utf-8
"""
抽取跟用户标签相对应的文章
"""

import pymysql
import xlrd
import xlwt
from random import sample

def get_labels():
	with open("data/user_label", 'r') as f:
		lines = f.readlines()
		labels = [line.strip() for line in lines]

	return labels

def get_url_content():
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select content, display_url from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("------共有{0}篇文章-------".format(len(results)))


	contents = [result[0] for result in results]
	urls = [result[1] for result in results]

	cursor.close()
	conn.close()

	return contents, urls

def get_label_urls(label, contents, urls):
	label_urls = []
	for i in range(len(urls)):
		if label in contents[i]:
			label_urls.append(urls[i])
		if len(label_urls) == 5:
			break

	return label_urls

def get_labels_urls_dict(labels, contents, urls):
	print("------获取标签对应的url-------")
	labels_urls_dict = {}
	for label in labels:
		labels_urls_dict[label] = get_label_urls(label, contents, urls)

	return labels_urls_dict

def get_users_labels():
	data = xlrd.open_workbook('data/100人标签.xlsx')
	table = data.sheets()[0]
	users_labels = table.col_values(0)

	return users_labels

def get_users_urls(users_labels, labels_urls_dict):
	print("-----获取用户对应的url-----")
	users_urls = []
	for user_labels in users_labels:
		user_urls = []
		user_labels_list = user_labels.split(",")
		for label in user_labels_list:
			label_urls = labels_urls_dict[label]
			user_urls = user_urls + label_urls
		if len(user_urls) <= 5:
			users_urls.append(user_urls)
		else:
			users_urls.append(sample(user_urls, 5))

	return users_urls

def save_urls(users_labels, users_urls):
	print("-----保存用户标签及url------")
	workbook = xlwt.Workbook(encoding='ascii')
	worksheet = workbook.add_sheet("user_label_url")

	for i in range(len(users_labels)):
		user_labels = users_labels[i]
		worksheet.write(i, 0, label=user_labels)
		user_urls = users_urls[i]
		for j in range(len(user_urls)):
			user_url = user_urls[j]
			worksheet.write(i, j+1, label=user_url)

	workbook.save('data/100人标签_资讯.xls')

if __name__ == "__main__":
	labels = get_labels()
	contents, urls = get_url_content()
	labels_urls_dict = get_labels_urls_dict(labels, contents, urls)
	users_labels = get_users_labels()
	users_urls = get_users_urls(users_labels, labels_urls_dict)
	save_urls(users_labels, users_urls)