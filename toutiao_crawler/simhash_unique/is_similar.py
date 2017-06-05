# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: check the similarity of 2 documents by VSM+cosine distance or simhash+hamming distance
"""

from simhash_imp import SimhashBuilder, hamming_distance
import jieba_word_seg
from features import FeatureBuilder, feature_single
import os
import clean_spec
from dict_builder import WordDictBuilder
from Utils import norm_vector_nonzero


class DocFeatLoader:
	def __init__(self, simhash_builder, feat_nonzero):
		self.feat_vec = feat_nonzero
		self.feat_vec = norm_vector_nonzero(self.feat_vec)
		self.fingerprint = simhash_builder.sim_hash_nonzero(self.feat_vec)


def gen_fp_all():
	# Clean all files
	os.chdir("../data")

	for file in os.listdir():
		# judge the original files
		if file[-1].isdigit():
			clean_spec.myfun(file)

	# Segment all files
	print('word segment...')

	for file in os.listdir():
		if "_clean" in file:
			infile = file
			outfile = file + "_cut"
			jieba_word_seg.engine(infile, outfile)

	# Build word dict
	filelist = []
	for file in os.listdir():
		if "_cut" in file:
			filelist.append(file)
	builder = WordDictBuilder(filelist=filelist)
	builder.run()
	builder.save("word_dict")

	# Load word dict
	word_list = []
	word_dict = {}
	with open("word_dict", 'r') as ins:
		for line in ins.readlines():
			word_list.append(line.split()[1])
			word_dict[line.split()[1]] = int(line.split()[0])

	# Build features of all files
	fb = FeatureBuilder(word_dict)
	print('Loaded', len(word_dict), 'words')
	for file in os.listdir():
		if "_cut" in file:
			feature_single(fb, file, file + "_feat")

	# Init simhash_builder and generate fingerprint of all files
	smb = SimhashBuilder(word_list)

	for file in os.listdir():
		if "_feat" in file:
			with open(file, 'r') as f:
				doc_feat = f.readlines()[0].strip().split()
				doc_feat = [(int(item.split(':')[0]), float(item.split(':')[1])) for item in doc_feat]
				doc_fp = DocFeatLoader(smb, doc_feat)
				with open(file + "_fp", 'w') as g:
					g.write(str(doc_fp.fingerprint))


def judge(dist, i, j, threshold):
	if dist < float(threshold):
		print('content{0} and content{1} matching Result:\t<True:{2}>'.format(str(i), str(j), dist))
	else:
		print('content{0} and content{1} matching Result:\t<False:{2}>'.format(str(i), str(j), dist))

if __name__ == "__main__":
	gen_fp_all()

	# os.chdir("../data")
	# print('Matching by Simhash + hamming distance')
	#
	# file_number = 5
	#
	# for i in range(1, file_number+1):
	# 	for j in range(i+1, file_number):
	# 		file1 = "content" + str(i) + "_clean_cut_feat_fp"
	# 		file2 = "content" + str(j) + "_clean_cut_feat_fp"
	# 		doc1_fp = int(open(file1, 'r').read().strip())
	# 		doc2_fp = int(open(file2, 'r').read().strip())
	# 		dist = hamming_distance(doc1_fp, doc2_fp)
	# 		judge(dist, i, j, threshold = 4)
