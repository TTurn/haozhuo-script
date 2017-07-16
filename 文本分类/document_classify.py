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

	def get_mi_features(self):

		with open("../data/chi_square_feat", 'r', encoding='utf8') as f:
			mi_features = list(set([line.strip() for line in f.readlines()]))

		return mi_features

	def cat_count(self):
		cat_num = defaultdict(int)

		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1230', db='39health',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select information_labels_ids from sample"
		cursor.execute(sql)
		conn.commit()

		labels = cursor.fetchall()
		length = len(labels)
		labels = labels[:length-50]
		print("---正在统计类别数目---")
		for i in labels:
			label_list = i[0].split(",")

			for label in label_list:
				cat_num[label] += 1
		return cat_num

	def cat_prob(self, cat_num):
		cat_prob_dict = dict()
		cat_num_sum = sum(cat_num.values())
		print("---正在计算类别概率---")
		for cat, num in cat_num.items():

			cat_prob_dict[cat] = num/cat_num_sum

		return cat_prob_dict

	def feat_cat_count(self, tf_idf_features):
		# 格式{C1:{F1:num,}, C2:{F1:num}}
		feat_cat_num = dict()

		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1230', db='39health',
							   charset='utf8')
		cursor = conn.cursor()

		sql = "select count(information_id) from sample"
		cursor.execute(sql)
		conn.commit()
		length = cursor.fetchall()[0][0]

		sql = "select content, information_labels_ids from sample"
		cursor.execute(sql)
		conn.commit()

		print("---正在计算特征/类别数目---")
		# for i in range(length-int(length/20)):
		for i in range(length-50):
			content_label = cursor.fetchone()
			content = BeautifulSoup(content_label[0], 'lxml').get_text()
			labels = content_label[1].split(",")
			# 关键点，features要set掉！
			features = set(self.get_features(content).split())

			for feature in features:
				if feature not in tf_idf_features:
					continue

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
		print("---正在计算特征/类别概率---")
		for cat, features in feat_cat_num.items():

			assumed_prob = cat_prob_dict[cat]
			for feature in features:
				# 关键点：除以类别中文章的个数！
				basic = features[feature]/cat_num[cat]
				total = self.get_feat_total(feat_cat_num, feature)
				# 关键点：修正概率，加权平均
				weigthed_prob = (weight*assumed_prob+basic*total)/(weight+total)
				feat_in_cat_prob[cat+" "+feature] = weigthed_prob

		return feat_in_cat_prob

	def doc_prob(self, content, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features, weight=1.0):
		doc_cat = {}
		features = set(self.get_features(content).split())

		for cat in cat_prob:
			doc_prob_single = cat_prob[cat]
			assumed_prob = cat_prob[cat]
			for feature in features:
				# 关键点：如果类别里没有这个特征的话，也要加个先验概率，直接continue相当于乘以1
				if feature not in tf_idf_features:
					continue

				if (cat+" "+feature) not in feat_in_cat_prob:
					total = self.get_feat_total(feat_cat_num, feature)
					# 避免0的出现，平滑
					weighted_prob = (weight*assumed_prob+0*total)/(weight+total)
					feat_in_cat_prob[cat+" "+feature] = weighted_prob

				doc_prob_single *= feat_in_cat_prob[cat+" "+feature]
			doc_cat[cat] = doc_prob_single
			"""for key in doc_cat.keys():
			if key != "#82#" or key != "#3#":
				doc_cat[key] = doc_cat[key] * 10"""

		sorted_doc_cat = sorted(doc_cat.items(), key=operator.itemgetter(1), reverse=True)
		return sorted_doc_cat


	def predict(self, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features):
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1230', db='39health',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select information_id, content from sample"
		cursor.execute(sql)
		conn.commit()

		id_contents = cursor.fetchall()

		length = len(id_contents)

		# id_contents = id_contents[length-int(length/20)-1:]
		id_contents = id_contents[length-50:]


		for id_content in id_contents:
			id = id_content[0]
			print("---正在计算类别/文档概率")
			content = BeautifulSoup(id_content[1],'lxml').get_text()

			print("------"+str(id)+"--------")
			print(self.doc_prob(content, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features))

		cursor.close()
		conn.close()

	def save(self,id, label):
		conn = pymysql.connect(host='192.168.1.162', port=3306, user='datag', passwd='yjkdatag', db='yjk_data_etl',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "update  toutiao_app_combine_unique_20170623 set information_labels_ids = %s where id = %s"
		cursor.execute(sql,(label,id))
		conn.commit()
		cursor.close()
		conn.close()

	def pred(self, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features):
		conn = pymysql.connect(host='192.168.1.162', port=3306, user='datag', passwd='yjkdatag', db='yjk_data_etl',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select id, htmls from toutiao_app_combine_unique_20170623"
		cursor.execute(sql)
		conn.commit()

		id_contents = cursor.fetchall()

		for id_content in id_contents:
			id = id_content[0]
			print("---正在计算类别/文档概率")
			content = BeautifulSoup(id_content[1], 'lxml').get_text()

			print("------" + str(id) + "--------")
			labels = self.doc_prob(content, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features)
			print(labels)
			label = labels[0][0]
			print("存储文章id：{0}".format(id))
			if label == "#1#":
				label = "减肥"
			if label == "#3#":
				label = "慢病"
			if label == "#82#":
				label = "养生"
			if label == "#83#":
				label = "男性"
			if label == "#84#":
				label = "女性"
			self.save(id, label)


if __name__ == "__main__":
	docclassify = Classifier()
	cat_num = docclassify.cat_count()     #获得训练集 类别数目
	print(cat_num)
	tf_idf_features = docclassify.get_mi_features()     #获得tf-idf 特征
	cat_prob_dict = docclassify.cat_prob(cat_num)        #计算类别概率
	feat_cat_num = docclassify.feat_cat_count(tf_idf_features)    #获得 特征在 类别中 的 数目
	feat_cat_prob = docclassify.weighted_feat_cat_prob(feat_cat_num, cat_num, cat_prob_dict)   #计算特征在类别中的概率
	docclassify.predict(cat_prob_dict, feat_cat_prob, feat_cat_num, tf_idf_features)    #测试后五十篇
	#docclassify.pred(cat_prob_dict, feat_cat_prob, feat_cat_num, tf_idf_features)     #线下文本分类
