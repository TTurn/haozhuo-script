# coding: utf-8
"""
Created on 2017-06-08
@author: He Youqiang
@brief: transfer examples to test environment to get training set
"""

import pymysql

def get_samples():
	"""
	抽取样本
	"""
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler', charset='utf8')
	cursor = conn.cursor()
	sql = "select title, abstract, htmls, display_url, id from toutiao_app_combine_unique_20170608"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	cursor.close()
	conn.close()

	return results

def load_samples(results):
	"""
	把样本插入测试数据库
	"""
	type = 0
	status = 0
	url_type = 0
	basic_label_ids = "#16#,#17#,#14#,#15#,#13#,#18#,#19#,#20#,#21#,#22#,#23#,#24#"
	disease_label_ids = "#44#,#42#,#66#,#93#"
	image = "empty"
	images = "empty"


	conn = pymysql.connect(host='192.168.1.170', port=3306, user='yjk_user', passwd='yjkuser33#', db='yjk',
						   charset='utf8')
	cursor = conn.cursor()

	# 暂时导入1000篇文章
	for i in range(1000):
		result = results[i]
		title = result[0]
		abstract = result[1]
		html = result[2]
		display_url = result[3]
		id = result[4]
		print("存入第{0}篇文章 {1}".format(i, id))

		sql = "INSERT INTO information (type, status, url_type, title, content, url," \
			  "detail, basic_label_ids, disease_label_ids, image, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (type, status, url_type, title, abstract, display_url, html, basic_label_ids, disease_label_ids, image, images)

		cursor.execute(sql, values)

	conn.commit()
	cursor.close()
	conn.close()

if __name__ == "__main__":
	results = get_samples()
	load_samples(results)

