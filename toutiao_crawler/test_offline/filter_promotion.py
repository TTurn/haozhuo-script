# coding: utf-8
"""
filter promotion  by regex
"""

import pymysql
from bs4 import BeautifulSoup

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler', charset='utf8')
	cursor = conn.cursor()


	sql = "select id, content, htmls from toutiao_app_combine_unique_20170620 where content regexp '热线|微信|公众号|头条号'"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("共有{0}个差样本".format(len(results)))

	cursor.close()
	conn.close()

	id_list = [result[0] for result in results]
	contents = [result[1] for result in results]
	htmls = [result[2] for result in results]

	return id_list, contents, htmls


def get_promotion_part():
	with open("data/news_promotion_part.txt") as f:
		lines = f.readlines()
		promotion_list = [line.strip() for line in lines]

	return promotion_list

def judge_promotion(promotion_list, content):
	delete_promotion = []
	for promotion in promotion_list:
		if promotion in content:
			delete_promotion.append(promotion)

	return delete_promotion

def filter(id_list, contents, htmls, promotion_list):

	revise_num = 1
	delete_num = 1

	for i in range(len(id_list)):
		print("正在过滤第{0}篇文章".format(i+1))
		id = id_list[i]
		content = contents[i]
		delete_promotion = judge_promotion(promotion_list, content)

		if not delete_promotion:
			print("正在删除第{0}篇文章".format(delete_num))
			# 如果我们总结的特殊字段在内容中没有，那么这个资讯直接删掉
			delete_news(id)
			delete_num += 1
		else:
			html = htmls[i]
			print("正在修正第{0}篇文章".format(revise_num))
			# 如果我们总结的特殊字段在内容中有，那么这个资讯要修正
			for promotion in delete_promotion:
				content_clean = content.replace(promotion, "")
				html_clean = sub_html(html, promotion)
			revise_news(id, content_clean, html_clean)
			revise_num += 1

def sub_html(html, promotion):
	soup = BeautifulSoup(html, 'lxml')
	for _ in soup.find_all("p"):
		if promotion in _.get_text():
			_.decompose()

	return str(soup)

def delete_news(id):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()
	sql = "delete from toutiao_app_combine_unique_20170620 where id = %s"
	cursor.execute(sql, (id,))
	conn.commit()
	cursor.close()
	conn.close()

def revise_news(id, content_clean, html_clean):
	conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='he123456', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	sql = "update toutiao_app_combine_unique_20170620 set content = %s, htmls = %s where id = %s"
	cursor.execute(sql, (content_clean, html_clean, id))
	conn.commit()

	cursor.close()
	conn.close()


if __name__ == "__main__":
	id_list, contents, htmls = get_samples()
	promotion_list = get_promotion_part()
	# id_list = [1896]
	# contents = ["点击右上角立即关注，更多健康内容不再错过，不定期惊喜送给你眼睛既是心灵的窗户，也是人体健康的镜子。通过观察眼部的症状，可以反映出疾病情况，有助于早发现、早治疗，防患于未然。　疾病在发生之初，往往都会向人体发出信号，如果不加以重视，就可能会酿成大病。　1、眼睛充血：眼结膜上布满了毛细血管，一旦血管破裂，就会有充血现象。眼科专家提醒，通常结膜出血没有明显原因，但如果患有严重高血压或血小板缺乏等疾病时，结膜也会充血。　2、眼睛凸出：甲亢时甲状腺激素水平异常，会使得眼部周围组织肿胀，眼睛像凸出来一样。　3、眼睑下垂：随着年龄增长，多数人会眼睑下垂。但美国加利福尼亚大学眼科临床副教授安德鲁指出，这也可能是脑部肿瘤或者重症肌无力的信号。　4、瞳孔异常：正常情况下，左右瞳孔应该是对称的。如果瞳孔一大一小或者一侧收缩的速度较慢、幅度较小，就可能是中风、脑肿瘤、视神经肿瘤等疾病的前期症状。　5、角膜环：这可能是威尔逊氏病的病症。由于此病患者的铜代谢存在障碍，导致铜沉积角膜上，在瞳孔周围形成一个“角膜环”。　6、眼睑增厚：眼睑增厚可能是神经纤维瘤的表现。　7、眼球变黄：肝炎和肝硬化等肝功能异常都会引起胆红素积聚，导致巩膜变黄。胆红素是血红蛋白的代谢产物，功能不正常时，胆红素无法正常排出，就会在体内聚积。　8、眼部血管斑：患有动脉粥样硬化的患者，一旦在视网膜毛细血管里发现细小的黄色斑块，则说明动脉粥样硬化已经很严重了。　9、视神经异常：在正常情况下，视神经应该呈粉红色，如果颜色变为浅白色，则可能是脑肿瘤、多发性硬化等疾病的征兆。　10、视网膜病变：包括糖尿病、高血压在内的很多疾病都会损伤视网膜上的血管和神经。因此，视网膜渗血、分泌黄色液体、出现白斑等，就应该立即做全身检查。"]
	# htmls = ['<html><body><div class="article-content"><div><p><strong>点击右上角立即关注，更多健康内容不再错过，不定期惊喜送给你</strong></p><p>眼睛既是心灵的窗户，也是人体健康的镜子。通过观察眼部的症状，可以反映出疾病情况，有助于早发现、早治疗，防患于未然。</p><p>　疾病在发生之初，往往都会向人体发出信号，如果不加以重视，就可能会酿成大病。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="447" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057584994371.png"/>　</p><p>1、眼睛充血：眼结膜上布满了毛细血管，一旦血管破裂，就会有充血现象。眼科专家提醒，通常结膜出血没有明显原因，但如果患有严重高血压或血小板缺乏等疾病时，结膜也会充血。</p><p>　2、眼睛凸出：甲亢时甲状腺激素水平异常，会使得眼部周围组织肿胀，眼睛像凸出来一样。</p><p>　3、眼睑下垂：随着年龄增长，多数人会眼睑下垂。但美国加利福尼亚大学眼科临床副教授安德鲁指出，这也可能是脑部肿瘤或者重症肌无力的信号。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="445" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057587182612.png"/>　</p><p>4、瞳孔异常：正常情况下，左右瞳孔应该是对称的。如果瞳孔一大一小或者一侧收缩的速度较慢、幅度较小，就可能是中风、脑肿瘤、视神经肿瘤等疾病的前期症状。</p><p>　5、角膜环：这可能是威尔逊氏病的病症。由于此病患者的铜代谢存在障碍，导致铜沉积角膜上，在瞳孔周围形成一个“角膜环”。</p><p>　6、眼睑增厚：眼睑增厚可能是神经纤维瘤的表现。</p><p>　7、眼球变黄：肝炎和肝硬化等肝功能异常都会引起胆红素积聚，导致巩膜变黄。胆红素是血红蛋白的代谢产物，功能不正常时，胆红素无法正常排出，就会在体内聚积。</p><p>　8、眼部血管斑：患有动脉粥样硬化的患者，一旦在视网膜毛细血管里发现细小的黄色斑块，则说明动脉粥样硬化已经很严重了。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="225" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057589235547.png"/>　</p><p>9、视神经异常：在正常情况下，视神经应该呈粉红色，如果颜色变为浅白色，则可能是脑肿瘤、多发性硬化等疾病的征兆。</p><p>　10、视网膜病变：包括糖尿病、高血压在内的很多疾病都会损伤视网膜上的血管和神经。因此，视网膜渗血、分泌黄色液体、出现白斑等，就应该立即做全身检查。</p></div></div></body></html>']
	filter(id_list, contents, htmls, promotion_list)