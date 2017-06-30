#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/27 9:18
# @Author  : Tuhailong
# @Site    : 
# @File    : 39health.py
# @Software: PyCharm Community Edition

import requests
from bs4 import BeautifulSoup
import pymysql
from get_proxy import GetProxy

def page_url_manager():
	init_page_url = "http://jbk.39.net/bw_t1"
	page_url_list = []
	page_url_list.append(init_page_url)

	for i in range(779):  # 疾病的页数 可以通过网页分析获得
		page_url = init_page_url + "_p" + str(i+1) + "#ps"
		page_url_list.append(page_url)

	return page_url_list

def download_page(url):
	headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q = 0.8",
		"Accept-Encoding":"gzip,deflate,sdch",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Host":"jbk.39.net",
		"Referer":"http://jbk.39.net/bw/",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0(Windows NT6.1;Win64;x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/58.0.3029.110 Safari/537.36"
	}
	try:
		#r = requests.get(url, headers = headers, proxies = proxy, otimeout = 10)
		r = requests.get(url, headers=headers, timeout=10)
		page_content = r.content
		return(page_content)

	except:
		print(url + "爬取超时")
		return False


def get_cat(page_content):
	"""
	得到一页疾病的名称和相应疾病的url
	"""
	soup = BeautifulSoup(page_content, 'lxml')
	cat_results = soup.find_all(class_='link')
	cat_num = len(cat_results)
	cat_url_list = []
	cat_name_list = []
	for i in range(cat_num):
		cat_result = cat_results[i].next_sibling.a
		cat_url = cat_result['href']
		cat_url_list.append(cat_url)
		cat_name = cat_result['title']
		cat_name_list.append(cat_name)

	return cat_name_list, cat_url_list


def download_article_page(articles_url):
	headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q = 0.8",
		"Accept-Encoding":"gzip,deflate,sdch",
		"Accept-Language":"zh-CN,zh;q = 0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Host":"jbk.39.net",
		"Referer":"http://jbk.39.net/yyz/",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0(Windows NT6.1;Win64;x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/58.0.3029.110 Safari/537.36"
	}
	try:
		#r = requests.get(articles_url,headers = headers, proxies = proxy, timeout = 10)
		r = requests.get(articles_url, headers=headers, timeout=10)
		article_page_content = r.content
		return article_page_content
	except:
		print(articles_url+"爬取超时")
		return False


def get_articles_url(soup):
	contents = soup.find_all(class_ = 'chr-artlist')[0]
	results = contents.find_all('ul')
	url_list = []
	is_expert_list = []
	for result in results:
		urls = result.find_all('a')
		for url in urls:
			href = url['href']
			expert = url.find_all('img')
			if len(expert) == 0:
				is_expert_list.append(0)
			else:
				is_expert_list.append(1)
			url_list.append(href)
	#print(is_expert_list)
	return url_list, is_expert_list


def download_article(url):
	headers = {
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Encoding":"gzip,deflate,sdch",
		"Accept-Language":"zh-CN,zh;q=0.8",
		"Cache-Control":"max-age=0",
		"Connection":"keep-alive",
		"Host":url.split('/')[2],
		"Referer":"http://jbk.39.net/yyz/all/art/1.shtml",
		"Upgrade-Insecure-Requests":"1",
		"User-Agent":"Mozilla/5.0(Windows NT 6.1;Win64;x64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	}
	try:
		print(url)
		#r = requests.get(url, headers = headers, proxies = proxy, timeout = 10)
		r = requests.get(url, headers=headers, timeout=10)
		soup = BeautifulSoup(r.content, "lxml")
		return soup
	except:
		print(url+"爬取超时")
		return False


def art_parse(soup, is_expert):
	try:
		#rank = soup.find_all(class_ = 'rank')[0].a.get_text()    #文章类别   名医专访、名医答疑、抑郁症...
		title = soup.find_all(class_ = 'art_box')[0].h1.get_text()
		date = soup.find_all(class_ = 'date')[0].em.get_text()
		source_soup_list = soup.find_all(class_ = 'date')[0].em.next_siblings
		source = ""
		for source_soup in source_soup_list:
			source += source_soup.get_text()
		#print(source)
	except:
		print("网页格式错误")      # http://ll.39.net/a/150717/4658569.html
		return []
	try:
		summary = soup.find_all(class_ = 'summary')[0].get_text()
	except:
		summary = ""
	if is_expert == 0:
		content = soup.find_all(class_ = 'art_con')[0].get_text()
	else:
		result = soup.find_all(class_ = 'art_con')[0]
		results = result.find_all('p')
		content = ""
		for item in results:
			content += item.get_text()
		#print(content)

	htmls = str(soup.find_all(class_ = 'art_con')[0])
	art_info = [title,date,source,summary,content,htmls]
	return art_info

def art_save(art_info):
	if len(art_info) != 3:
		#art_info[cat_name, is_expert, display_url, title, date, summary, content]
		conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
		cursor = conn.cursor()
		sql = "insert ignore into 39health_information(cat_name, is_expert, display_url, title, date, source, summary, content, htmls) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		print("正在存储文章"+art_info[2])
		cursor.execute(sql, art_info)


		conn.commit()
		cursor.close()
		conn.close()
	else:
		pass

def engine(page_url_list):
	for i in range(len(page_url_list)):  # 指定下载页
		print("正在爬取疾病类别第{0}页".format(i+1))
		page_url = page_url_list[i]
		page_content = download_page(page_url)  # 下载疾病页
		cat_name_list, cat_url_list = get_cat(page_content)  # 得到一页疾病的名称和相应疾病的url

		for k in range(len(cat_url_list)):
			cat_name = cat_name_list[k]
			print("正在爬取第{0}个疾病，疾病名称：{1}".format(k+1, cat_name))
			cat_url = cat_url_list[k]
			j = 1
			while True:
				article_page_url = cat_url + "all/art/" + str(j) + ".shtml"
				article_page_content = download_article_page(article_page_url)  # 下载文章列表页面

				# 查看该类别是否还有文章,没有了则跳出while
				try:
					articles_soup = BeautifulSoup(article_page_content, 'lxml')
					contents = articles_soup.find_all(class_='chr-artlist')[0]
					results = contents.find_all('ul')[0].li
					if results == None:  # 返回的页面没有文章
						break
				except:  # 由于爬取超时没有返回页面
					break
				art_url_list, is_expert_list = get_articles_url(articles_soup)  # 获取文章url和是否是专家栏目

				print("正在爬取疾病 {0} 的第{1}页资讯".format(cat_name, j))

				for l in range(len(art_url_list)):
					print("正在爬取疾病第{0}个资讯".format(l+1))
					article_soup = download_article(art_url_list[l])  # 下载文章
					art_info = art_parse(article_soup, is_expert_list[l])  # 解析文章
					art_info.insert(0, art_url_list[l])
					art_info.insert(0, is_expert_list[l])
					art_info.insert(0, cat_name)
					art_save(art_info)
				j += 1



if __name__ == "__main__":
	# get_proxy = GetProxy()
	# proxy = get_proxy.get_proxy()
	#print(proxy)

	page_url_list = page_url_manager()
	engine(page_url_list)