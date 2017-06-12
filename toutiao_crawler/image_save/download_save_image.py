# coding: utf-8
"""
Created on 2017-06-02
@author: He Youqiang
@brief: download source image and save them to upyun
"""

import requests
import time
import random
import pymysql
from bs4 import BeautifulSoup
import upyun
import multiprocessing

class DownloadSaveImage():
	def __init__(self):
		self.up = upyun.UpYun('yjk-article-image', 'datag', 'datag123')
		self.up.up_form.endpoint = upyun.ED_AUTO

	def download(self, url):
		"""
		下载图片，返回一个二进制序列
		"""
		pic = requests.get(url)

		# fp = open("/Users/mountain/Desktop/test.png", 'wb')
		# fp.write(pic.content)
		# fp.close()

		return pic.content

	def get_file_path(self):
		"""
		生成文件路径
		"""
		prefix = "http://article.image.ihaozhuo.com"
		date = time.strftime("%Y/%m/%d/", time.localtime())
		milli_time = str(int(round(time.time() * 1000)))
		end = str(random.randint(1000, 9999))

		path = "/" + date + milli_time + end + ".png"
		url = prefix + path

		return path, url

	def get_id_htmls(self):
		"""
		得到id,htmls
		"""
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "select id, htmls from toutiao_app_combine_20170608 where id > 27981"
		cursor.execute(sql)
		conn.commit()
		id_htmls = cursor.fetchall()

		cursor.close()
		conn.close()

		return id_htmls

	def get_image_src(self, html):
		"""
		把hmtl中的image source url抽取出来
		"""
		img_src_list = []
		soup = BeautifulSoup(html, 'lxml')
		img_list = soup.find_all('img')
		for img in img_list:
			img_src_list.append(img['src'])

		return img_src_list

	def replace_img_src(self, html, img_src_list, img_save_list):
		"""
		把html中的image source换成图片存储的位置
		"""
		for i in range(len(img_src_list)):
			html = html.replace(img_src_list[i], img_save_list[i])

		return html

	def update_html(self, id, html):
		"""
		把新生成的hmtl更新到数据库中
		"""
		conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
							   charset='utf8')
		cursor = conn.cursor()
		sql = "UPDATE toutiao_app_combine_20170608 SET htmls = %s WHERE id = %s"
		values = (html, id)
		cursor.execute(sql, values)
		conn.commit()

		cursor.close()
		conn.close()

	def upyun_save(self, content, path):

		headers = {'x-gmkerl-thumb': '/fw/300'}
		self.up.put(path, content, checksum=True, headers=headers)

	def engine_single(self, num, id, html):
		print("正在下载转换第{0}篇文章，id {1}".format(num + 1, id))
		img_src_list = self.get_image_src(html)
		for url in img_src_list:
			try:
				img_content = self.download(url)
			except:
				print("------图片不能下载------url:{0}".format(url))
				continue
			path_url = self.get_file_path()
			save_path = path_url[0]
			save_url = path_url[1]
			try:
				self.upyun_save(img_content, save_path)
			except:
				print("------图片不能存储------url:{0}".format(url))
				continue
			html = html.replace(url, save_url)
		self.update_html(id, html)

	def engine(self):
		id_htmls = self.get_id_htmls()
		pool = multiprocessing.Pool(multiprocessing.cpu_count())
		for num in range(len(id_htmls)):
			id_html = id_htmls[num]
			id = id_html[0]
			html = id_html[1]
			pool.apply_async(self.engine_single, (num, id, html))
			# self.engine_single(num, id, html)

			# if num == 2:
			# 	break

		pool.close()
		pool.join()




if __name__ == "__main__":
	dsi = DownloadSaveImage()
	dsi.engine()

	# size test
	# content = dsi.download("http://p1.pstatp.com/large/22c8000536885488a66b")
	# # content = dsi.download("http://p1.pstatp.com/large/242d0004f197f4932bd3")
	# path_url = dsi.get_file_path()
	# path = path_url[0]
	# url = path_url[1]
	# print(url)
	# dsi.upyun_save(content, path)


