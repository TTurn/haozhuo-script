# coding: utf-8
"""
Created on 2017-06-11
@author: He Youqiang
@brief: build feature dictionary according to word frequency
"""

from collections import defaultdict
import pymysql
from bs4 import BeautifulSoup
import jieba_word_seg
import operator

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	sql = "select detail from information"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	cursor.close()
	conn.close()

	return results

def get_word_dict(results):
	word_dict = defaultdict(int)
	i = 1
	for result in results:
		print("----转换第{0}个样本----".format(i))
		content = BeautifulSoup(result[0], 'lxml').get_text()
		content_seg = jieba_word_seg.engine(content).split()
		for word in content_seg:
			word_dict[word] += 1
		i += 1

	sorted_word_dict = sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)

	return sorted_word_dict

def save_word_dict(word_dict):

	f = open("../data/sample_word_dict", 'a')
	g = open("../data/features", 'a')

	for word, freq in word_dict:
		line = word + "\t" + str(freq) + "\n"
		f.write(line)
		g.write(word+"\n")

	f.close()
	g.close()


if __name__ == "__main__":
	results = get_samples()
	sorted_word_dict = get_word_dict(results)
	save_word_dict(sorted_word_dict)
