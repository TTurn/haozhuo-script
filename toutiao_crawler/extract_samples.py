# coding: utf-8

import pymysql
from random import sample
import xlwt

def get_random_urls():
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
	cursor = conn.cursor()
	sql = "select display_url from toutiao_app_combine_unique_20170608"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	urls = [result[0] for result in results]

	return sample(urls, 100)

def save_url(urls):
	data=xlwt.Workbook()
	table = data.add_sheet('0616')

	table.write(0, 0, "资讯原生链接")
	for i in range(len(urls)):
		print("-------{0}--------".format(i))
		url = urls[i]
		table.write(i+1, 0, url)

	data.save("资讯问题详细记录_运营_0616.xls")

if __name__ == "__main__":
	urls = get_random_urls()
	save_url(urls)


