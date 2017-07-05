# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: convert document to features
"""

import os,sys
class FeatureBuilder:
    def __init__(self, word_dict):
        self.word_dict = word_dict
    
    def compute(self, token_list):
        feature = [0]*len(self.word_dict)
        for token in token_list:
            feature[self.word_dict[token]] += 1
        feature_nonzero = [(idx, value) for idx, value in enumerate(feature) if value > 0]
        return feature_nonzero

    def _add_word(self, word):
        if not word in self.word_dict:
            self.word_dict[word] = len(self.word_dict)

    def update_words(self, word_list=[]):
        for word in word_list:
            self._add_word(word)

class FeatureBuilderUpdate(FeatureBuilder):
    def _add_word(self, word):
        self.word_dict.add_one(word)


def feature_single(instance, content):
    feature = instance.compute([token for token in content.strip().split()])
    l = []
    for idx,f in feature:
        if f > 1e-6:
            l.append('%s:%s' %(idx,f))
    feature_new = ' '.join(l)
    return feature_new

if __name__=="__main__":
    # if len(sys.argv) < 5:
    #     print "Usage:\tfeature.py -s/-m <word_dict_path> <tokens_file/tokens_folder> <feature_file/feature_folder>"
    #     exit(-1)
    os.chdir("../data")
    word_dict = {}
    with open("word_dict", 'r') as ins:
        for line in ins.readlines():
            l = line.split()
            word_dict[l[1]] = int(l[0])
    fb = FeatureBuilder(word_dict)
    print('Loaded', len(word_dict), 'words')
    # if sys.argv[1] == '-s':
    #     feature_single(sys.argv[3], sys.argv[4])
    # elif sys.argv[1] == '-m':
    #     for inputfile in os.listdir(sys.argv[3]):
    #         feature_single(os.path.join(sys.argv[3],inputfile), os.path.join(sys.argv[4],inputfile.replace('.token','.feat')))
    word_dict_path = "word_dict"
    tokens_file_list = []
    for file in os.listdir():
        if "_cut" in file:
            tokens_file_list.append(file)
    for inputfile in tokens_file_list:
        feature_single(instance=fb, inputfile=inputfile, outputfile=inputfile+"_feat")