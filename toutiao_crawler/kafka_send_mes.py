# coding: utf-8

from pykafka import KafkaClient
import pymysql
import json

def get_message(id):
	"""
	{
    "title": "xxx",
    "keywords": "xxx",
    "abstracts": "xxx",
    "content": "",
    "source": "xxx",
    "htmls": "xxx",
    "create_time": "2017-11-11 11:11:11",
    "crawler_time": "2017-11-11 11:11:11",
    "information_labels_ids": "xxx"
    }
	"""
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select title, keywords, abstract, content, source, htmls, create_time, crawler_time, information_labels_ids from toutiao_app_combine_unique_20170608 where id = %s"
	cursor.execute(sql, id)
	conn.commit()
	result = cursor.fetchall()[0]
	message = {"title": result[0], "keywords": result[1], "abstracts": result[2], "content": result[3], "source": result[4],
			   "htmls": result[5], "create_time": str(result[6]), "crawler_time": str(result[7]), "information_labels_ids": result[8]}

	return json.dumps(message, ensure_ascii=False)

def engine():
	test_ids = [29777, 2150, 37666, 1626, 29777, 2150, 37666, 1626, 29777, 2150, 37666, 1626]
	client = KafkaClient(hosts="192.168.1.152:9092, 192.168.1.153:9092")

	topic = client.topics['dev-dataetl-articlefilter'.encode('utf-8')]

	with topic.get_producer() as producer:
		for id in test_ids:
			print("---{0}---".format(id))
			mes = get_message(id)
			producer.produce(mes.encode('utf-8'))


if __name__ == "__main__":
	engine()