# coding: utf-8
"""
Created on 2017-06-04
@author: He Youqiang
@brief: convert content to fingerprint to perform simhash algorithm
"""

import pymysql
from clean_spec import clean
from jieba_word_seg import engine
from dict_builder import WordDictBuilderSingle
from collections import defaultdict
from features import FeatureBuilder, feature_single
from simhash_imp import SimhashBuilder
from is_similar import DocFeatLoader
import multiprocessing


def build_dict():
	"""
	生成word_dict
	"""
	# get length

	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
	cursor = conn.cursor()
	sql = "select count(id) from toutiao_app_combine_20170608"
	cursor.execute(sql)
	conn.commit()
	length = cursor.fetchall()[0][0]

	# get content
	sql = "select content from toutiao_app_combine_20170608"
	cursor.execute(sql)
	conn.commit()

	# 把词典暂时放在内存里
	word_dict = defaultdict(int)

	for i in range(length):
		content = cursor.fetchone()[0]
		print("正在抽取第{0}篇".format(i+1))
		content_clean = clean(content)
		content_seg = engine(content_clean)
		word_dict_builder = WordDictBuilderSingle(word_dict=word_dict, word_segment=content_seg)
		word_dict = word_dict_builder.run()

	cursor.close()
	conn.close()

	# 把词典存到文件中中
	word_dict_builder.save("../data/word_dict")

def gen_fp_single(word_seg):
	"""
	根据word_dict，把word_seg转换成fingerprint
	"""
	word_dict_path = "../data/word_dict"

	# Load word dict
	word_list = []
	word_dict = {}
	with open(word_dict_path, 'r') as ins:
		for line in ins.readlines():
			word_list.append(line.split()[1])
			word_dict[line.split()[1]] = int(line.split()[0])

	# Build feature
	fb = FeatureBuilder(word_dict)
	feature_new = feature_single(fb, word_seg)

	# Init simhash_builder and generate fingerprint
	smb = SimhashBuilder(word_list)

	doc_feat = feature_new.strip().split()
	doc_feat = [(int(item.split(':')[0]), float(item.split(':')[1])) for item in doc_feat]
	doc_fp = DocFeatLoader(smb, doc_feat)

	return doc_fp

def save_fp_single(i, result, cursor, conn):
	if result:
		id = result[0] if result[0] else ""
		content = result[1] if result[1] else ""
	else:
		id = ""
		content = ""
	print("正在转换第{0}篇的指纹 id:{1}".format(i + 1, id))
	# print(result)
	content_clean = clean(content)
	content_seg = engine(content_clean)
	try:
		content_fp = gen_fp_single(content_seg).fingerprint
	except:
		print("-------指纹获取失败error-------{0}".format(id))
	try:
		sql = "UPDATE toutiao_app_combine_20170608 SET fingerprint = %s WHERE id = %s"
		values = (content_fp, id)
		cursor.execute(sql, values)
		conn.commit()
	except:
		print("-------------out of range error------------{0}".format(id))


def save_fp_all():
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "select count(id) from toutiao_app_combine_20170608"
	cursor.execute(sql)
	conn.commit()
	length = cursor.fetchall()[0][0]

	# get content
	sql = "select id, content from toutiao_app_combine_20170608"
	cursor.execute(sql)
	conn.commit()
	results = cursor.fetchall()

	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	for i in range(length):
		result = results[i]
		save_fp_single(i, result, cursor, conn)
		# pool.apply_async(save_fp_single, (i, results, cursor, conn))

	pool.close()
	pool.join()

	cursor.close()
	conn.close()

if __name__ == "__main__":
	# build_dict()
	save_fp_all()