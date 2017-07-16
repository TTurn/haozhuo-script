#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/13 9:23
# @Author  : Tuhailong
# @Site    : 
# @File    : chi-square_filter.py
# @Software: PyCharm Community Edition
import pymysql
from bs4 import BeautifulSoup
import jieba_word_seg
import operator
import math

def get_samples():
    print("----获取样本----")
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1230', db='39health',
                           charset='utf8')
    cursor = conn.cursor()

    sql = "select content, information_labels_ids from sample"
    cursor.execute(sql)
    conn.commit()

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    contents = [BeautifulSoup(result[0], 'lxml').get_text() for result in results]
    labels = [result[1] for result in results]
    return contents, labels

def stop_words_filter():
    with open("../data/features", 'r',encoding='utf8') as f:
        feature_list = list(set([line.strip() for line in f.readlines()]))

    with open("../data/stop_words", 'r',encoding='utf8') as f:
        stop_word_list = [line.strip() for line in f.readlines()]

    for feat in feature_list:
        if feat in stop_word_list:
            feature_list.remove(feat)
    return feature_list

def engine(contents, labels, feature_list):
    cont2feat_list = []
    for i in range(len(contents)):
        print("文本分词")
        features = jieba_word_seg.engine(contents[i]).split()
        cont2feat_list.append(features)

    label_num = [0,0,0,0,0]            #计算每个类别的文章数目
    for i in range(len(labels)):
        if labels[i] == '#1#':
            label_num[0] += 1
        if labels[i] == '#3#':
            label_num[1] += 1
        if labels[i] == '#82#':
            label_num[2] += 1
        if labels[i] == '#83#':
            label_num[3] += 1
        if labels[i] == '#84#':
            label_num[4] += 1

    print("每个类别文章数目")
    print(label_num)
    label_list = ["#1#","#3#","#82#","#83#","#84#"]     #类别列表
    feat_chi_square = []

    i = 1
    for label in label_list:
        feat_chi_square_dict = {}
        print("第{0}类".format(i))
        for feat in feature_list:
            N1_ = 0
            N11 = 0
            N00 = 0
            N01 = 0
            N10 = 0
            N = (len(cont2feat_list))
            for i in range(len(cont2feat_list)):
                if feat in cont2feat_list[i]:
                    N1_ += 1
                    if labels[i] == label:
                        N11 += 1
                    else:
                        N10 += 1
                elif labels[i] != label:
                    N00 += 1
                else:
                    N01 += 1
            N_1 = N01 + N11
            N0_ = N - N1_
            print("N10:{0}".format(N10))
            print("N00:{0}".format(N00))
            N_0 = N00 + N10
            print("N:{0}".format(N))
            print("N1_:{0}".format(N1_))
            print("N_1:{0}".format(N_1))
            print("N0_:{0}".format(N0_))
            print("N_0:{0}".format(N_0))
            E10 = N1_ * N_0 / N
            E01 = N0_ * N_1 / N
            E00 = N0_ * N_0 / N
            E11 = N1_ * N_1 / N
            try:
                chi_square = pow(N00-E00,2)/E00 + pow(N01-E01,2)/E01 + pow(N10-E10,2)/E10 + pow(N11-E11,2)/E11
                feat_chi_square_dict[feat] = chi_square
            except:
                pass
        print(feat_chi_square_dict)
        sorted_feat_mi = sorted(feat_chi_square_dict.items(), key=operator.itemgetter(1), reverse=True)
        print(sorted_feat_mi[:20])
        feat_chi_square += sorted_feat_mi[:20]
        i += 1
    print(feat_chi_square)
    return feat_chi_square

def feat_save(feat_chi_square):
    print("----正在存储特征----")
    with open("../data/chi_square_feat", 'w',encoding='utf8') as f:
        for line in feat_chi_square:
            line = line[0]
            f.write(line+"\n")

if __name__ == "__main__":
    contents, labels = get_samples()
    feature_list = stop_words_filter()
    feat_chi_square = engine(contents, labels, feature_list)
    feat_save(feat_chi_square)