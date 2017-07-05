#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 10:14
# @Author  : Tuhailong
# @Site    : 
# @File    : get_cat.py
# @Software: PyCharm Community Edition

import requests
import pymysql
from bs4 import BeautifulSoup

def get_cat(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q = 0.8",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "jbk.39.net",
        "Referer": "http://jbk.39.net/bw/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0(Windows NT6.1;Win64;x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/58.0.3029.110 Safari/537.36"
    }
    r = requests.get(url,headers = headers, timeout = 10)
    soup = BeautifulSoup(r.content, "lxml")
    return(soup)

def parse_cat(soup):
    results = soup.find_all(class_ = "res_list")
    cat_list = []
    for result in results:
        cat_name = result.dt.h3.a.string
        cat_list.append(cat_name)
    return cat_list
def save_cat(cat_list):
    conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='39_crawler',
                           charset='utf8')
    #conn = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = '1230', db = '39health', charset = 'utf8')
    cursor = conn.cursor()
    sql = "insert ignore into cat_information (cat_name) values (%s)"
    for j in range(len(cat_list)):
        print(cat_list[j])
        cursor.execute(sql,cat_list[j])
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    for i in range(780):
        if i == 0:
            url = "http://jbk.39.net/bw_t1/"
        else:
            url = "http://jbk.39.net/bw_t1_p"+str(i)+"#ps"

        print("正在爬取第{0}页疾病类别".format(i+1))
        soup = get_cat(url)
        print("正在分析第{0}页疾病类别".format(i+1))
        cat_list = parse_cat(soup)
        print("正在存储第{0}页疾病类别".format(i+1))
        save_cat(cat_list)

