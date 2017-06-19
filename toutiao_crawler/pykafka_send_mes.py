# coding: utf-8

from pykafka import KafkaClient

client = KafkaClient(hosts="192.168.1.152:9092, 192.168.1.153:9092")

topic = client.topics['dev-dataetl-articlefilter'.encode('utf-8')]

with topic.get_producer() as producer:
	producer.produce('test message'.encode('utf-8'))