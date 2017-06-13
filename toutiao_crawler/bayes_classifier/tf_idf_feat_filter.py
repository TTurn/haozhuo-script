# coding: utf-8
"""
Created on 2017-06-13
@author: He Youqiang
@brief: use tf/idf to filter features
"""

import pymysql
import jieba_word_seg
from collections import Counter
from bs4 import BeautifulSoup
from math import log
import operator

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	sql = "select detail from information"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	cursor.close()
	conn.close()

	contents = [BeautifulSoup(result[0], 'lxml').get_text() for result in results]

	return contents

def feat_count_list(content):
	"""
	统计一篇文章中特征的个数
	"""
	features = jieba_word_seg.engine(content).split()
	features_list = Counter(features)

	return features_list

def feat_doc_count_list(contents):
	"""
	统计所有文章中特征个数
	"""
	feat_in_doc_list = []
	i = 1
	for content in contents:
		print("统计第{0}篇文章中特征个数".format(i))
		features_list = feat_count_list(content)
		feat_in_doc_list.append(features_list)
		i += 1

	return feat_in_doc_list

def idf_compute(feat, feat_in_doc_list):
	feat_in_doc_num = 0
	for feat_in_doc in feat_in_doc_list:
		if feat in feat_in_doc:
			feat_in_doc_num += 1

	return log(len(feat_in_doc_list))-log(1+feat_in_doc_num)

def tf_idf_sort(content, feat_in_doc_list):
	"""
	计算一个文章中的所有特征的tf/idf，返回最高的10个
	"""
	feature_tf_idf = {}
	features_list = feat_count_list(content)
	total_df = sum(features_list.values())
	for feature in features_list:
		tf = features_list[feature]/total_df
		idf = idf_compute(feature, feat_in_doc_list)
		feature_tf_idf[feature] = tf*idf

	sorted_feature_tf_idf = sorted(feature_tf_idf.items(), key=operator.itemgetter(1), reverse=True)

	if len(sorted_feature_tf_idf) > 5:
		sorted_feature_tf_idf = sorted_feature_tf_idf[:5]

	return sorted_feature_tf_idf

def tf_idf_sort_save(sorted_feature_tf_idf):
	with open("../data/tf_idf_feat", 'a') as f:
		for i in sorted_feature_tf_idf:
			f.write(i[0]+"\n")

def unique_save_feat():
	with open("../data/tf_idf_feat", 'r') as f:
		lines = list(set([line.strip() for line in f.readlines()]))
	with open("../data/tf_idf_feat_uniq", 'w') as f:
		for line in lines:
			f.write(line+"\n")


def engine(contents, feat_in_doc_list):
	for content in contents:
		sorted_feature_tf_idf = tf_idf_sort(content, feat_in_doc_list)
		tf_idf_sort_save(sorted_feature_tf_idf)



if __name__ == "__main__":
	contents = get_samples()
	feat_in_doc_list = feat_doc_count_list(contents)
	engine(contents, feat_in_doc_list)
	# unique_save_feat()