# coding: utf-8
"""
Created on 2017-05-30
@author: He Youqiang
@brief: crawl health news from Toutiao app and save them to MySQL
@version: Anaconda Python 3.6, MySQL 5.7
"""

import requests
import json
from bs4 import BeautifulSoup
import pymysql
from select_proxy import SelectProxy
from get_proxy import GetProxy
import time
import multiprocessing
import re
from datetime import datetime
from datetime import timedelta
from image_save.download_save_image import DownloadSaveImage
from pykafka import KafkaClient


def download_page(proxy):
	"""
	根据Charles抓包数据，下载页面数据，转换为json格式，
	里面包含文章url，便于进行下一层爬取。
	重复抓取，重复刷新。
	"""
	url = "https://lf.snssdk.com/api/news/feed/v53/?version_code=6.1.2&app_name=news_article&vid=644F80DA-8C14-4012-9312-AD3FD7E4771D&device_id=35432641928&channel=App%20Store&resolution=750*1334&aid=13&ab_version=132023,126063,132049,122834,130106,131380,126066,132364,126072,131619,131542,125502,125174,132469,132400,127333,130386,126059,132482,121513,132027,122948,130200,130932,131077,131207,114338,127757&ab_feature=z1&openudid=1710bbf8e661ee837482b8501c84606968eb1fc1&live_sdk_version=1.6.5&idfv=644F80DA-8C14-4012-9312-AD3FD7E4771D&ac=WIFI&os_version=10.3.1&ssmix=a&device_platform=iphone&iid=10608408767&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=31856174-9926-4EE8-8230-F626A85DCC4D&LBS_status=deny&category=news_health&city=%E6%9D%AD%E5%B7%9E&concern_id=6215497895248923137&count=20&cp=559f24F5E1135q1&detail=1&image=1&language=zh-Hans-CN&last_refresh_sub_entrance_interval=3198&loc_mode=0&min_behot_time=1496309541&refer=1&strict=0&tt_from=pull"
	# url = "https://lf.snssdk.com/api/news/feed/v53/?category=news_health&concern_id=6215497895248923137&refer=1&count=20&min_behot_time=&last_refresh_sub_entrance_interval=&loc_mode=0&tt_from=enter_auto&cp=569419a4d874dq1&iid=10291744168&device_id=36372853508&ac=wifi&channel=xiaomi&aid=13&app_name=news_article&version_code=612&version_name=6.1.2&device_platform=android&ab_version=125481%2C124685%2C126064%2C124993%2C125842%2C127421%2C126035%2C114040%2C122834%2C126065%2C125865%2C123727%2C127188%2C127130%2C126071%2C125839%2C126791%2C125503%2C125174%2C127527%2C127333%2C104321%2C126058%2C127138%2C126401%2C126526%2C126125%2C122948%2C123125%2C31244%2C127080%2C126153%2C121011%2C125527%2C126014%2C114338%2C127485%2C125065&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=Redmi+Note+4&device_brand=Xiaomi&language=zh&os_api=23&os_version=6.0&uuid=862963032864841&openudid=c7ef43d7c65a8f17&manifest_version_code=612&resolution=1080*1920&dpi=480&update_version_code=6124&_rticket="
	headers = {"Host": "lf.snssdk.com",
			   "Accept": "*/*",
			   # "X-SS-Cookie": "install_id=10608408767; ttreq=1$30f9a8db4a7a7b5b6945b3dd28fa6bf1289d0d83; alert_coverage=45; qh[360]=1; _ga=GA1.2.791888771.1496287081; _gid=GA1.2.2032824666.1496287081",
			   # "tt-request-time": "1496310069163",
			   # "Cookie": "install_id=10608408767; ttreq=1$30f9a8db4a7a7b5b6945b3dd28fa6bf1289d0d83; alert_coverage=45; qh[360]=1; _ga=GA1.2.791888771.1496287081; _gid=GA1.2.2032824666.1496287081",
			   "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; Mi-4c MIUI/V8.2.3.0.NXKCNEC) NewsArticle/6.2.1 okhttp/3.4.1.4",
			   "Accept-Language": "zh-Hans-CN;q=1, en-CN;q=0.9, zh-Hant-CN;q=0.8",
			   "Accept-Encoding": "gzip, deflate",
			   "Connection": "keep-alive"
			   }
	# time.sleep(3)
	try:
		# r = requests.get(url, headers=headers, proxies=proxy, timeout=10)
		r = requests.get(url, headers=headers, timeout=10)
	except requests.exceptions.ConnectionError:
		time.sleep(600)

	return json.loads(r.content)

def download_article(url, proxy):
	"""
	下载文章具体数据，返回html string
	"""
	headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Accept-Encoding":"gzip, deflate, sdch",
				"Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
				"Cache-Control":"max-age=0",
				"Connection":"keep-alive",
			   # "Cookie":'uuid="w:0679fa3956ec4a25b1df0c6f1414f644"; UM_distinctid=15c0f85c307917-0393925375c7e1-396a7807-13c680-15c0f85c3083c6; utm_campaign=client_share; utm_medium=toutiao_ios; tt_webid=58898935764; csrftoken=4e4b8c67d5c0d158fb6e187d70eee007; utm_source=toutiao; __tasessionId=4c9bhk63n1496318497849; _ba=BA0.2-20170601-51d9e-JYRWTIu0eUXHHeFyq7nD; CNZZDATA1259612802=1234287108-1494904209-https%253A%252F%252Fwww.google.com%252F%7C1496314101; _ga=GA1.2.357536120.1494909044; _gid=GA1.2.1507970231.1496318870',
			   # "Cookie":'uuid="w:0679fa3956ec4a25b1df0c6f1414f644"; UM_distinctid=15c0f85c307917-0393925375c7e1-396a7807-13c680-15c0f85c3083c6; tt_webid=58898935764; __utma=24953151.357536120.1494909044.1497862244.1497870184.7; __utmc=24953151; __utmz=24953151.1497525300.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); csrftoken=4e4b8c67d5c0d158fb6e187d70eee007; _ba=BA0.2-20170601-51d9e-JYRWTIu0eUXHHeFyq7nD; __tasessionId=318opm6uk1497875205076; _ga=GA1.2.357536120.1494909044; _gid=GA1.2.189065431.1497843875; CNZZDATA1259612802=1234287108-1494904209-https%253A%252F%252Fwww.google.com%252F%7C1497873569',
				"Host":"www.toutiao.com",
				"Upgrade-Insecure-Requests":"1",
				"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
				}
	try:
		# time.sleep(3)
		# r = requests.get(url, headers=headers, proxies=proxy, timeout=20)
		r = requests.get(url, headers=headers, timeout=10)
		return r.content.decode('utf-8')
	except:
		print(url + "  爬取超时")
		return False

def parse_page(content):
	"""
	根据页面得到的json格式数据，抽取title,
	keywords, abstract, display_url, source等字段
	"""
	results = []
	for data in content['data']:
		result = {}
		keys = ['title', 'keywords', 'abstract', 'display_url', 'source']
		article =json.loads(data['content'])

		# 问答类、广告类暂时不要
		try:
			if article['source'] == "头条问答" or 'http://toutiao.com' not in article['display_url']:
				continue
		except:
			print("页面解析有错误")
			continue

		for key in keys:
			result[key] = article[key] if key in article else " "
		results.append(result)

	return results

def get_image_list(soup):
	image_list = []

	for _ in soup.find_all('img'):
		image_list.append(_['src'])

	# 图片不要发太多，少发几个！！
	if len(image_list) > 3:
		image_list = image_list[:3]

	return image_list

def get_comment_count(soup):
	for tag in soup.find_all("script"):
		pattern = re.compile("\d+")
		if "utils.numCutByComma" in tag.get_text():
			line = tag.get_text().split("\n")[4]
			comment_count = re.search(pattern, line).group()
			return comment_count

	return False

def judge_by_title(title):
	pattern = re.compile("执业|执医|执照|狗|猪|通知|培训|养殖|多少钱")

	return re.search(pattern, title)

def judge_by_content(content):
	pattern = re.compile("兽医|taobao|jd|投票|官网")

	return re.search(pattern, content)

def judge_by_source(source):
	pattern = re.compile("养殖|猪|电台|阅读|重疾不重|禽|兽")

	return re.search(pattern, source)

def judge_conference(content, create_time, init=0.15):
	"""
	基于时间和发布时间比较及特殊字段来判断是否是通讯
	"""

	pattern1 = re.compile('([0-9]{4}年)\d{1,2}月\d{1,2}日')  # 年 月 日
	pattern3 = re.compile('会议|论坛|通知|通讯|记者|讯|举办|举行|活动|开展')

	timedelta1 = timedelta(days=-3)
	timedelta2 = timedelta(days=3)

	length = len(content)

	# 根据字段判断
	match3 = pattern3.search(content[:int(init * length)])
	if match3:
		return True

	match1 = pattern1.search(content[:int(init * length)])
	if match1:
		date_raw = match1.group()
		date_std = date_raw.replace(r'年', '-').replace(r'月', '-').replace(r'日', '')
		try:
			date_std = datetime.strptime(date_std, "%Y-%m-%d")
		except:
			date_spec = date_std.split('-')
			year = int(date_spec[0])
			month = int(date_spec[1])
			day = int(date_spec[2])
			date = str(year) + '-' + str(month) + '-' + str(day)
			date_std = datetime.strptime(date, "%Y-%m-%d")

		if timedelta1 < date_std - create_time < timedelta2:
			return True

	return False

def judge_short(content):

	length = len(content)
	if length < 400:
		return True

	return False

def judge_image_interlink(content):
	"""
	检查图片中是否包含内链
	"""
	pattern = re.compile("pgc-card .pgc-card-href")

	return re.search(pattern, content)

def sub_image_interlink_content(content):
	content_clean = re.sub("#pgc(.*?)购买", "", content, flags=re.S)

	return content_clean

def sub_image_interlink_html(html):
	soup = BeautifulSoup(html, 'lxml')
	for _ in soup.find_all("style"):
		_.decompose()
	for _ in soup.find_all(class_=re.compile("pgc.*")):
		_.decompose()

	return str(soup)

def judge_html_promotion(html):
	pattern = re.compile("热线|微信|公众号|头条号|公号|公-众-号|微 信|二维码|关注|点击|咨询|联系方式|订阅|授权|转载|转自|邮箱|访问|网址|网站|文章来源|链接|报名|网 址|出处|官网|下载地址|原文|图片来源|图片来自|文章来自|了解更多|欢迎登录|为您推荐|详情|参考文献|精心推荐|详细新闻|中康体检|文章推荐|参考资料|文献参考|电话|版权|文图：|编辑：")
	return re.search(pattern, html)


def sub_html_promotion(html):
	soup = BeautifulSoup(html, 'lxml')
	promotion_list = ["热线", "微信", "公众号", "头条号", "公号", "公-众-号", "微 信", "关注", "二维码", "联系方式", "订阅", "点击", "咨询", "授权", "转载", "转自", "邮箱", "访问", "网址", "网站", "文章来源", "报名", "链接", "网 址", "出处", "官网", "下载地址", "原文", "图片来源", "图片来自", "文章来自", "了解更多", "欢迎登录", "为您推荐", "详情", "参考文献", "精心推荐", "详细新闻", "中康体检", "文章推荐", "参考资料", "文献参考", "电话", "版权", "文图：", "编辑："]

	# 包含推广，则整段整段删除
	for _ in soup.find_all(re.compile("p|h1")):
		for promotion in promotion_list:
			if promotion in _.get_text():
				_.decompose()

	return str(soup)

def me_filter(content):
	"""
	清楚我过多的资讯
	"""
	pattern1 = re.compile('我们')
	pattern2 = re.compile('我')

	match1 = pattern1.findall(content)
	num_we = len(match1)
	match2 = pattern2.findall(content)
	num_me = len(match2)

	if num_me - num_we >= 12:
		return True

	return False

def url_filter(content):
	# url识别的正则表达式
	pattern = re.compile('[\(|（|\[|①|②|③|：]?(https|http|www){1}(:|\.|[a-z]|\d|_|[A-Z]|/| |\?|%|=|&|#|;)+[\)|）|\]|］]?')

	match = re.search(pattern, content)

	if match:
		spec = match.group()
		return spec
	else:
		return False

def parse_article(results, proxy, dsi):
	"""
	根据display_url，得到html，抽取content, htmls,
	create_time等字段
	"""
	# 把错误的文章内容记下来，最后删除
	wrong_results = []

	for i in range(len(results)):
		print("正在爬取第{0}篇文章".format(i+1))
		display_url = results[i]['display_url']
		article_html = download_article(display_url, proxy)

		# 如果article_html返回的是False,说明download超时了
		if not article_html:
			wrong_results.append(results[i])
			continue
		soup = BeautifulSoup(article_html, 'lxml')
		try:
			# 常规字段添加
			results[i]['create_time'] = soup.find_all(class_='time')[0].get_text()

			# create_time归一化！！
			if len(results[i]['create_time']) < 19:
				results[i]['create_time'] = results[i]['create_time'] + ":00"

			results[i]['content'] = soup.find_all(class_='article-content')[0].get_text()
			results[i]['htmls'] = str(soup.find_all(class_='article-content')[0])
			news_class = soup.find_all(ga_event="click_channel")[0].get_text()

			# 主题不是健康的去除！！不能放前面，不然等会remove去除不好去除。保险起见。可优化
			if news_class == "健康":
				news_label_list = ",".join(soup.find_all(class_="label-list")[0].get_text().split())
				# 添加原生资讯的主题，标签
				results[i]['raw_class'] = news_class
				results[i]['raw_label'] = news_label_list
			else:
				wrong_results.append(results[i])
				continue  # continue直接跳出这一次循环，然后通过wrong_results在后面把这个残缺的result去除

			# 过滤文字中包含推广的，只修正html，content不修正
			if judge_html_promotion(results[i]['htmls']):
				# 如果有特殊字段，则清洗节点
				results[i]['htmls'] = sub_html_promotion(results[i]['htmls'])


			# 界面没有评论字段的去除！！
			comment_count = get_comment_count(soup)
			if comment_count:
				results[i]['comment_count'] = comment_count
			else:
				wrong_results.append(results[i])
				continue

			# 去除文本内容很少的
			if not judge_short(results[i]['content']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 去除会议新闻，基于时间判断
			if not judge_conference(results[i]['content'], results[i]['create_time']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 根据标题清除
			if not judge_by_title(results[i]['title']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 根据内容清除
			if not judge_by_content(results[i]['content']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 根据来源清除
			if not judge_by_source(results[i]['source']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 我过多的资讯清除
			if not me_filter(results[i]['content']):
				pass
			else:
				wrong_results.append(results[i])
				continue

			# 过滤文本中包含url的，然后只改html，content不改！！
			# 有多个url，重复替换！！
			spec = 1
			j = 1
			while spec:
				spec = url_filter(results[i]['content'])
				if not spec:
					break
				results[i]['htmls'] = results[i]['htmls'].replace(spec, "")
				results[i]['content'] = BeautifulSoup(results[i]['htmls'], 'lxml').get_text()
				j += 1
				# 链接过多的，直接当做坏文本
				if j == 5:
					wrong_results.append(results[i])
					break

			if j == 5:
				continue


			# 修正图片里面包含内链的
			if judge_image_interlink(results[i]['content']):
				results[i]['content'] = sub_image_interlink_content(results[i]['content'])
				results[i]['htmls'] = sub_image_interlink_html(results[i]['htmls'])

			# 替换图片链接
			img_src_list = dsi.get_image_src(results[i]['htmls'])
			for url in img_src_list:
				try:
					img_content = dsi.download(url)
				except:
					# print("------图片不能下载------url:{0}".format(url))
					continue
				path_url = dsi.get_file_path()
				save_path = path_url[0]
				save_url = path_url[1]
				try:
					dsi.upyun_save(img_content, save_path)
				except:
					# print("------图片不能存储------url:{0}".format(url))
					continue
				results[i]['htmls'] = results[i]['htmls'].replace(url, save_url)


			# 添加image_thumbnail和image_list
			# 这里要重新soup一遍，千万别忘了！！
			soup = BeautifulSoup(results[i]['htmls'], 'lxml')
			image_list = get_image_list(soup)
			image_thumbnail = image_list[0] if image_list else ""
			image_list = ",".join(image_list) if image_list else ""
			results[i]["image_thumbnail"] = image_thumbnail
			results[i]["image_list"] = image_list

			# 最后把content换成html的
			results[i]['content'] = BeautifulSoup(results[i]['htmls'], 'lxml').get_text()

			# 空摘要的要添加上
			if len(results[i]['abstract']) < 20:
				results[i]['abstract'] = results[i]['content'][:50]

		except:
			print(results[i]['display_url'] + "  为问答或广告")
			wrong_results.append(results[i])
			continue

	for wrong in wrong_results:
		results.remove(wrong)



	return results

def save(results):
	"""
	存储结果到MySQL
	"""
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
	cursor = conn.cursor()
	sql = "INSERT IGNORE INTO toutiao_app_combine_unique_20170623 (title, keywords, abstract, content, source," \
		  "display_url, htmls, create_time, raw_class, raw_label, image_thumbnail, image_list, comment_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	result_num = 1
	for result in results:
		print("正在存储第{0}篇文章".format(result_num))
		result_num += 1
		values = (result['title'], result['keywords'], result['abstract'], result['content'], result['source'],
				  result['display_url'], result['htmls'], str(result['create_time']), result['raw_class'], result['raw_label'],
				  result['image_thumbnail'], result['image_list'], result['comment_count'])
		try:
			cursor.execute(sql, values)
		except:
			print(result['display_url'] + "  存储失败")
	conn.commit()
	cursor.close()
	conn.close()

def send_kafka(results):
	"""
	发送消息给kafka
	"""
	client = KafkaClient(hosts="10.169.152.113:9092, 10.169.152.109:9092, 10.30.192.98:9092")

	topic = client.topics['dev-dataetl-articlefilter'.encode('utf-8')]

	with topic.get_producer() as producer:
		for i in range(len(results)):
			result = results[i]
			print("正在发送第{0}篇文章".format(i+1))
			# 如果图片为空，不发送卡夫卡消息，但是数据库仍然要存
			if result['image_thumbnail'] == "":
				break

			result['crawler_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
			message = {"title": result['title'], "abstracts": result['abstract'], "source": result['source'],
					   "htmls": result['htmls'], "create_time": str(result['create_time']), "image_thumbnail": result['image_thumbnail'], "image_list": result['image_list'],
					   "content": result['content'], "display_url": result['display_url'], "crawler_time": result['crawler_time']}
			message_std = json.dumps(message, ensure_ascii=False)

			producer.produce(message_std.encode('utf-8'))

def engine(page, proxy):
	"""
	不停刷新，不停爬数据
	"""
	content = download_page(proxy)
	results = parse_page(content)
	# if len(results) == 0:
	# 	continue
	dsi = DownloadSaveImage()
	print("------正在爬取第{0}页文章，共{1}个------".format(page+1, len(results)))
	results_more = parse_article(results, proxy, dsi)
	print("------正在存储第{0}页文章，共{1}个------".format(page+1, len(results)))
	save(results_more)
	print("------正在发送第{0}页文章，共{1}个------".format(page+1, len(results)))
	send_kafka(results_more)


# 图片存储问题，路径映射
# 去重
if __name__ == "__main__":
	# selectproxy = SelectProxy(100)
	# selectproxy.engine()
	get_proxy = GetProxy()
	pool = multiprocessing.Pool(multiprocessing.cpu_count())

	# 改造成多进程
	for page in range(10000):
		# engine(page)
		if page % 25 == 0:
			proxy = get_proxy.get_proxy()
		engine(page, proxy)
		# pool.apply_async(engine, (page, proxy))
	pool.close()
	pool.join()
