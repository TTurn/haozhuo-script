# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: use jieba to perform word segmentation with custom stopwords and nature
"""

import jieba
import jieba.posseg as pseg
import os

def load_dict(dict_path):
	for dict in os.listdir(dict_path):
		jieba.load_userdict(dict_path + "/" + dict)

def engine(content):
	word_seg = ""
	stopwords_nature = ["m", "mq", "mg", "b", "begin", "bg", "bl", "c", "cc", "e", "end", "o", "p", "pba", "pbei", "q",
						"qt", "qv", "u", "ude1", "ude2", "ude3", "udeng", "udh", "uguo", "ule", "ulian", "uls", "usuo",
						"uyy", "uzhe", "uzhi", "y", "z", "r", "rr", "ry", "rys", "ryt", "ryv", "rz", "rzs", "rzt",
						"rzv", "w", "nx"]
	with open("../data/stop_words", "r") as f:
		stopwords = [x.strip() for x in f.readlines()]

	word_nature = pseg.cut(content)
	for word, nature in word_nature:
		if (word not in stopwords) and (nature not in stopwords_nature) and not word.isdigit():
			word_seg = word_seg + word + " "

	return word_seg

if __name__ == "__main__":

	pass
