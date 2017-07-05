#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/30 15:47
# @Author  : Tuhailong
# @Site    : 
# @File    : filter.py
# @Software: PyCharm Community Edition
import pymysql
import re
from bs4 import BeautifulSoup

def get_samples():
    conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='39_crawler',
                           charset='utf8')
    #conn = pymysql.connect(host = '127.0.0.1', port = 3306,user = 'root',passwd = '1230', db = '39health', charset = 'utf8')
    cursor = conn.cursor()

    sql = "select id, htmls from 39health_information"
    cursor.execute(sql)
    conn.commit()
    results = cursor.fetchall()

    id_list = [result[0] for result in results]
    html_list = [result[1] for result in results]
    cursor.close()
    conn.close()

    return id_list, html_list

def filter(id_list, html_list):
    for i in range(len(id_list)):
        id = id_list[i]
        print(id)
        html = html_list[i]
        html_clean = sub_html(html)
        revise_news(id, html_clean)

def sub_html(html):
    filter_word_list = ["想知道如何预防疾病？","以上是本文章的全部内容，要了解更多可用微信扫描下方二维码。"]      # 过滤条件
    soup = BeautifulSoup(html, 'lxml')
    for _ in soup.find_all(re.compile("p")):
        for filter_word1 in filter_word_list:
            if filter_word1 in _.get_text():
                item_list = []
                for item in _.next_siblings:
                    item_list.append(item)
                for item in item_list:
                    item.extract()
                _.extract()

    #去除  相关疾病
    result = soup.find_all('p')[-1]
    content = result.get_text()

    filter_word_list = ["相关疾病","友情提醒"]      #过滤条件
    for filter_word in filter_word_list:
        if filter_word in content:
        #print(result)
            result.extract()

    for _ in soup.find_all("img"):
        #print(_)
        if 'alt' in _.attrs:
            if _['alt'] == "疾病百科底部广告":     #过滤条件
                #print(_)
                _.extract()

    result = str(soup)
    result = result.replace("39健康网：","问题:")                     #过滤条件
    result = result.replace("39健康网编辑：","问题:")
    result = result.replace("39健康网","")

    return result

def revise_news(id, html_clean):
    conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='39_crawler',
                           charset='utf8')
    #conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1230', db='39health',charset='utf8')
    cursor = conn.cursor()

    sql = "update 39health_information set htmls = %s where id = %s"
    cursor.execute(sql, (html_clean, id))

    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    id_list, html_list = get_samples()
    filter(id_list, html_list)
