# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: build feature dictionary according to word frequency
"""

from collections import defaultdict
import os
import sys


class WordDictBuilder:
	def __init__(self, ori_path='', filelist=[], tokenlist=[]):
		self.word_dict = defaultdict(int)
		if ori_path != '' and os.path.exists(ori_path):
			with open(ori_path) as ins:
				for line in ins.readlines():
					self.word_dict[line.split('\t')[1]] = int(line.split('\t')[2])
		self.filelist = filelist
		self.tokenlist = tokenlist

	def run(self):
		for filepath in self.filelist:
			self._updateDict(filepath)
		self._updateDictByTokenList()
		return self

	def _updateDict(self, filepath):
		with open(filepath, 'r') as ins:
			for line in ins.readlines():
				for word in line.rstrip().split():
					self.word_dict[word] += 1

	def _updateDictByTokenList(self):
		for token in self.tokenlist:
			# if isinstance(token, unicode):
			#     token = token.encode('utf8')
			self.word_dict[token] += 1

	def save(self, filepath):
		l = [(value, key) for key, value in self.word_dict.items()]
		l = sorted(l, reverse=True)
		result_lines = []
		for idx, (value, key) in enumerate(l):
			result_lines.append('%s\t%s\t%s%s' % (idx, key, value, os.linesep))
		with open(filepath, 'w') as outs:
			outs.writelines(result_lines)

class WordDictBuilderSingle:
	def __init__(self, word_dict, word_segment):
		self.word_dict = word_dict
		self.word_segment = word_segment

	def run(self):
		self._updateDict(self.word_segment)
		return self.word_dict

	def _updateDict(self, word_segment):
		for word in word_segment.strip().split():
			self.word_dict[word] += 1

	def save(self, filepath):
		l = [(value, key) for key, value in self.word_dict.items()]
		l = sorted(l, reverse=True)
		result_lines = []
		for idx, (value, key) in enumerate(l):
			result_lines.append('%s\t%s\t%s%s' % (idx, key, value, os.linesep))
		with open(filepath, 'w') as outs:
			outs.writelines(result_lines)

if __name__ == "__main__":
	pass
	# if len(sys.argv) < 3:
	#     print "Usage:\tWordDictBuilder.py <input_folder/file> <output_file>"
	#     exit(-1)
	# if not os.path.isfile(sys.argv[1]):
	#     filelist = [sys.argv[1] + os.sep + f for f in os.listdir(sys.argv[1])]
	# else:
	#     filelist = [sys.argv[1]]
	# os.chdir("../data")
	# filelist = []
	# for file in os.listdir():
	# 	if "_cut" in file:
	# 		filelist.append(file)
	# builder = WordDictBuilder(filelist=filelist)
	# builder.run()
	# builder.save("word_dict")