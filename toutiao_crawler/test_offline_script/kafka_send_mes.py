# coding: utf-8

from pykafka import KafkaClient
import pymysql
import json
import time
from random import sample

def get_message(id):
	"""
	{"title": "string",
  "abstracts": "string",
  "source": "string",
  "htmls": "string",
  "create_time": "time",
  "image_thumbnail": "string",
  "image_list": "string",
  "content": "string",
  "display_url": "string",
  "crawler_time": "time"}
	"""
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select title, abstract, source, htmls, create_time, image_thumbnail, image_list, content, display_url, crawler_time from toutiao_app_combine_unique_20170623 where id = %s"
	cursor.execute(sql, id)
	conn.commit()
	result = cursor.fetchall()[0]

	# create_time归一化！！
	# result[4] = str(result[4])
	# if len(result[4]) < 19:
	# 	result[4] = result[4] + ":00"

	message = {"title": result[0], "abstracts": result[1], "source": result[2],
			   "htmls": result[3], "create_time": str(result[4]), "image_thumbnail": result[5], "image_list": result[6], "content": result[7], "display_url": result[8], "crawler_time": str(result[9])}

	return json.dumps(message, ensure_ascii=False)

def get_id_list():
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select id from toutiao_app_combine_unique_20170623 where image_thumbnail <> ''"
	cursor.execute(sql)
	conn.commit()
	results = cursor.fetchall()
	id_list = [result[0] for result in results]

	# return sample(id_list, 1000)
	return id_list

def engine(id_list):
	# client = KafkaClient(hosts="10.169.152.113:9092, 10.169.152.109:9092, 10.30.192.98:9092")
	client = KafkaClient(hosts="192.168.1.153:9092")

	topic = client.topics['dev-dataetl-articlefilter'.encode('utf-8')]

	with topic.get_producer() as producer:
		for i in range(len(id_list)):
			id = id_list[i]
			print("---正在发送第{0}篇文章给kafka---".format(i+1))
			# time.sleep(1)
			mes = get_message(id)
			producer.produce(mes.encode('utf-8'))
			# if i == 15:
			# 	break


if __name__ == "__main__":
	id_list = get_id_list()
	engine(id_list)