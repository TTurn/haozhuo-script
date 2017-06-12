# coding: utf-8
"""
Created on 2017-06-08
@author: He Youqiang
@brief: naive bayes document classifier
"""

import jieba_word_seg
from collections import defaultdict
import pymysql
from bs4 import BeautifulSoup
import operator


class Classifier():
	"""
	训练分类器
	"""
	def __init__(self):
		self.get_features = jieba_word_seg.engine

	def cat_count(self):
		cat_num = defaultdict(int)

		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select information_labels_ids from information"
		cursor.execute(sql)
		conn.commit()

		labels = cursor.fetchall()

		length = len(labels)

		labels = labels[:length-12]

		for i in labels:
			label_list = i[0].split(",")
			print("---正在统计类别数目---")
			for label in label_list:
				cat_num[label] += 1

		return cat_num

	def cat_prob(self, cat_num):
		cat_prob_dict = dict()
		cat_num_sum = sum(cat_num.values())
		for cat, num in cat_num.items():
			print("---正在计算类别概率---")
			cat_prob_dict[cat] = num/cat_num_sum

		return cat_prob_dict

	def feat_cat_count(self):
		# 格式{C1:{F1:num,}, C2:{F1:num}}
		feat_cat_num = dict()

		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
		cursor = conn.cursor()

		sql = "select count(information_id) from information"
		cursor.execute(sql)
		conn.commit()
		length = cursor.fetchall()[0][0]

		sql = "select detail, information_labels_ids from information"
		cursor.execute(sql)
		conn.commit()


		for i in range(length-12):
			content_label = cursor.fetchone()
			content = BeautifulSoup(content_label[0], 'lxml').get_text()
			labels = content_label[1].split(",")
			# 关键点，features要set掉！
			features = set(self.get_features(content).split())
			for feature in features:
				print("---正在计算特征/类别数目---")
				for label in labels:
					if label not in feat_cat_num:
						feat_cat_num[label] = defaultdict(int)
					feat_cat_num[label][feature] += 1

		return feat_cat_num

	def get_feat_total(self, feat_cat_num, feat):
		total = 0

		for cat, features in feat_cat_num.items():
			if feat in features:
				total += features[feat]

		return total

	def weighted_feat_cat_prob(self, feat_cat_num, cat_num, cat_prob_dict, weight=1.0):
		feat_in_cat_prob = dict()

		for cat, features in feat_cat_num.items():
			print("---正在计算特征/类别概率---")
			assumed_prob = cat_prob_dict[cat]
			for feature in features:
				# 关键点：除以类别中文章的个数！
				basic = features[feature]/cat_num[cat]
				total = self.get_feat_total(feat_cat_num, feature)
				weigthed_prob = (weight*assumed_prob+basic*total)/(weight+total)
				feat_in_cat_prob[cat+" "+feature] = weigthed_prob

		return feat_in_cat_prob

	def doc_prob(self, content, cat_prob, feat_in_cat_prob, feat_cat_num, weight=1.0):
		doc_cat = {}
		features = set(self.get_features(content).split())

		for cat in cat_prob:
			doc_prob_single = cat_prob[cat]
			assumed_prob = cat_prob_dict[cat]
			for feature in features:
				# 关键点：如果类别里没有这个特征的话，也要加个先验概率，直接continue相当于乘以1
				if (cat+" "+feature) not in feat_in_cat_prob:
					total = self.get_feat_total(feat_cat_num, feature)
					weighted_prob = (weight*assumed_prob+0*total)/(weight+total)
					feat_in_cat_prob[cat+" "+feature] = weighted_prob

				doc_prob_single *= feat_in_cat_prob[cat+" "+feature]
			doc_cat[cat] = doc_prob_single

		sorted_doc_cat = sorted(doc_cat.items(), key=operator.itemgetter(1), reverse=True)

		return sorted_doc_cat

	def predict(self, cat_prob, feat_in_cat_prob, feat_cat_num):
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select information_id, detail from information"
		cursor.execute(sql)
		conn.commit()

		id_contents = cursor.fetchall()

		length = len(id_contents)

		id_contents = id_contents[length-12:]

		for id_content in id_contents:
			id = id_content[0]
			content = BeautifulSoup(id_content[1],'lxml').get_text()
			print("---正在计算类别/文档概率")
			print("------"+str(id)+"--------")
			print(self.doc_prob(content, cat_prob, feat_in_cat_prob, feat_cat_num))


if __name__ == "__main__":
	docclassify = Classifier()
	cat_num = docclassify.cat_count()
	cat_prob_dict = docclassify.cat_prob(cat_num)
	feat_cat_num = docclassify.feat_cat_count()
	feat_cat_prob = docclassify.weighted_feat_cat_prob(feat_cat_num, cat_num, cat_prob_dict)
	docclassify.predict(cat_prob_dict, feat_cat_prob, feat_cat_num)