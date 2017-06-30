# coding: utf-8
"""
Created on 2017-06-08
@author: He Youqiang
@brief: naive bayes document classifier
"""

from collections import defaultdict
import operator


class Classifier():
	"""
	训练分类器
	"""
	def __init__(self):
		pass

	def get_features(self):
		features = []
		with open("../data/dc_demo", 'r') as f:
			for line in f.readlines():
				features = features + line.strip().split(",")[0].split()

		return list(set(features))

	def get_labels(self):
		with open("../data/dc_demo", 'r') as f:
			labels = [line.strip().split(",")[1] for line in f.readlines()]

		return labels

	def get_contents(self):
		with open("../data/dc_demo", 'r') as f:
			contents = [line.strip().split(",")[0] for line in f.readlines()]

		return contents


	def cat_count(self, labels):
		cat_num = defaultdict(int)

		for label in labels:
			cat_num[label] += 1

		return cat_num

	def cat_prob(self, cat_num):
		cat_prob_dict = dict()
		cat_num_sum = sum(cat_num.values())
		for cat, num in cat_num.items():
			cat_prob_dict[cat] = num/cat_num_sum

		return cat_prob_dict

	def feat_cat_count(self, contents, labels):
		# 格式{C1:{F1:num,}, C2:{F1:num}}
		feat_cat_num = dict()

		for i in range(len(labels)):
			content = contents[i]
			label = labels[i]

			features = list(set(content.split()))

			for feature in features:
				if feature not in features:
					continue
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
				# 关键点：修正概率，加权平均
				weigthed_prob = (weight*assumed_prob+basic*total)/(weight+total)
				feat_in_cat_prob[cat+" "+feature] = weigthed_prob

		return feat_in_cat_prob

	def doc_prob(self, content, cat_prob, feat_in_cat_prob, feat_cat_num, tf_idf_features, weight=1.0):
		doc_cat = {}
		features = set(content.split())

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

		sorted_doc_cat = sorted(doc_cat.items(), key=operator.itemgetter(1), reverse=True)

		return sorted_doc_cat

	def predict(self, cat_prob, feat_in_cat_prob, feat_cat_num, features):
			content = input("Enter the content you want to test: ")
			print(self.doc_prob(content, cat_prob, feat_in_cat_prob, feat_cat_num, features))


if __name__ == "__main__":
	dc_demo = Classifier()
	features = dc_demo.get_features()
	labels = dc_demo.get_labels()
	contents = dc_demo.get_contents()
	cat_num = dc_demo.cat_count(labels)
	cat_prob_dict = dc_demo.cat_prob(cat_num)
	feat_cat_num = dc_demo.feat_cat_count(contents, labels)
	feat_cat_prob = dc_demo.weighted_feat_cat_prob(feat_cat_num, cat_num, cat_prob_dict)
	dc_demo.predict(cat_prob_dict, feat_cat_prob, feat_cat_num, features)