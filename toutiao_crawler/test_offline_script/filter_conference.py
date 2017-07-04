# coding: utf-8
"""
filter conference and news by regular
"""
import pymysql
import re
from datetime import datetime
from datetime import timedelta

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
	cursor = conn.cursor()

	sql = "select id from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()
	length = len(cursor.fetchall())
	print("共有{0}个样本".format(length))

	sql = "select id, title, content, create_time from toutiao_app_combine_unique_20170623"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	cursor.close()
	conn.close()

	id_list = [result[0] for result in results]
	contents = [result[1]+result[2] for result in results]
	create_time_list = [result[3] for result in results]

	return id_list, contents, create_time_list


def filter(id_list, contents, create_time_list, init=0.15):

	pattern1 = re.compile(r'([0-9]{4}年)\d{1,2}月\d{1,2}日')  # 年 月 日
	pattern2 = re.compile(r'\d{1,2}月\d{1,2}日')    #月 日
	pattern3 = re.compile(r'会议|论坛|通知|通讯|记者|讯|举办|举行|活动|开展')

	delete_id_list = []
	timedelta1 = timedelta(days=-3)
	timedelta2 = timedelta(days=3)

	for i in range(len(contents)):
		print("正在解析第{0}篇文章".format(i+1))

		content = contents[i]
		length = len(content)

		match3 = pattern3.search(content[:int(init * length)])
		if match3:
			delete_id_list.append(id_list[i])
			continue

		match1 = pattern1.search(content[:int(init * length)])
		if match1:
			date_raw = match1.group()
			date_std = date_raw.replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
			try:
				date_std = datetime.strptime(date_std, "%Y-%m-%d")
			except:
				date_spec = date_std.split('-')
				year = int(date_spec[0])
				month = int(date_spec[1])
				day = int(date_spec[2])
				date = str(year) + '-' + str(month) + '-' + str(day)
				date_std = datetime.strptime(date, "%Y-%m-%d")

			create_time = create_time_list[i]
			if timedelta1 < date_std - create_time < timedelta2:
				delete_id_list.append(id_list[i])
				continue

		# match2 = pattern2.search(content[:int(init * length)])
		# if match2:
		# 	date_raw = match2.group()
		# 	date_std = date_raw.replace(r'月', '-').replace(r'日', '')
		# 	try:
		# 		date_std = "2017-" + date_std
		# 		date_std = datetime.strptime(date_std, "%Y-%m-%d")
		# 	except:
		# 		date_spec = date_std.split('-')
		# 		month = int(date_spec[1])
		# 		day = int(date_spec[2])
		# 		date_std = "2017-" + str(month) + '-' + str(day)
		# 		date_std = datetime.strptime(date_std, "%Y-%m-%d")

			create_time = create_time_list[i]
			if timedelta1 < date_std - create_time < timedelta2:
				delete_id_list.append(id_list[i])
				continue

	return delete_id_list
	# print(delete_id_list)
	# print(len(delete_id_list))

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
	id_list, contents, create_time_list = get_samples()  # content:[str,str,...]
	delete_id_list = filter(id_list, contents, create_time_list)
	delete_news(delete_id_list)

