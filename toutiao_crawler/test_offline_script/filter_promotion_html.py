# coding: utf-8
"""
filter promotion  by regex
"""

import pymysql
from bs4 import BeautifulSoup
import re

def get_samples():
	print("----获取样本----")
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler', charset='utf8')
	cursor = conn.cursor()


	sql = "select id, htmls from toutiao_app_combine_unique_20170623 where htmls regexp '热线|微信|公众号|头条号|公号|公-众-号|微 信|二维码|关注|点击|咨询|联系方式|订阅|授权|转载|转自|邮箱|访问|网址|网站|文章来源|链接|报名|网 址|出处|官网|下载地址|原文|图片来源|图片来自|文章来自|了解更多|欢迎登录|为您推荐|详情|参考文献|精心推荐|详细新闻|中康体检|文章推荐|参考资料|文献参考|电话|版权'"
	cursor.execute(sql)
	conn.commit()

	results = cursor.fetchall()

	print("共有{0}个差样本".format(len(results)))

	cursor.close()
	conn.close()

	id_list = [result[0] for result in results]
	htmls = [result[1] for result in results]

	return id_list, htmls

def filter(id_list, htmls):


	for i in range(len(id_list)):
		print("正在过滤第{0}篇文章".format(i+1))
		id = id_list[i]
		html = htmls[i]
		html_clean = sub_html(html)
		revise_news(id, html_clean)


def sub_html(html):
	promotion_list = ["热线", "微信", "公众号", "头条号", "公号", "公-众-号", "微 信", "关注", "二维码", "联系方式", "订阅", "点击", "咨询", "授权", "转载", "转自", "邮箱", "访问", "网址", "网站", "文章来源", "报名", "链接", "网 址", "出处", "官网", "下载地址", "原文", "图片来源", "图片来自", "文章来自", "了解更多", "欢迎登录", "为您推荐", "详情", "参考文献", "精心推荐", "详细新闻", "中康体检", "文章推荐", "参考资料", "文献参考", "电话", "版权"]

	soup = BeautifulSoup(html, 'lxml')
	for _ in soup.find_all(re.compile("p|h1")):
		for promotion in promotion_list:
			if promotion in _.get_text():
				_.decompose()

	return str(soup)

def revise_news(id, html_clean):
	conn = pymysql.connect(host='116.62.106.69', port=3306, user='datag', passwd='yjkdatag', db='news_crawler',
						   charset='utf8')
	cursor = conn.cursor()

	sql = "update toutiao_app_combine_unique_20170623 set htmls = %s where id = %s"
	cursor.execute(sql, (html_clean, id))
	conn.commit()

	cursor.close()
	conn.close()


if __name__ == "__main__":
	id_list, htmls = get_samples()
	# id_list = [1896]
	# contents = ["点击右上角立即关注，更多健康内容不再错过，不定期惊喜送给你眼睛既是心灵的窗户，也是人体健康的镜子。通过观察眼部的症状，可以反映出疾病情况，有助于早发现、早治疗，防患于未然。　疾病在发生之初，往往都会向人体发出信号，如果不加以重视，就可能会酿成大病。　1、眼睛充血：眼结膜上布满了毛细血管，一旦血管破裂，就会有充血现象。眼科专家提醒，通常结膜出血没有明显原因，但如果患有严重高血压或血小板缺乏等疾病时，结膜也会充血。　2、眼睛凸出：甲亢时甲状腺激素水平异常，会使得眼部周围组织肿胀，眼睛像凸出来一样。　3、眼睑下垂：随着年龄增长，多数人会眼睑下垂。但美国加利福尼亚大学眼科临床副教授安德鲁指出，这也可能是脑部肿瘤或者重症肌无力的信号。　4、瞳孔异常：正常情况下，左右瞳孔应该是对称的。如果瞳孔一大一小或者一侧收缩的速度较慢、幅度较小，就可能是中风、脑肿瘤、视神经肿瘤等疾病的前期症状。　5、角膜环：这可能是威尔逊氏病的病症。由于此病患者的铜代谢存在障碍，导致铜沉积角膜上，在瞳孔周围形成一个“角膜环”。　6、眼睑增厚：眼睑增厚可能是神经纤维瘤的表现。　7、眼球变黄：肝炎和肝硬化等肝功能异常都会引起胆红素积聚，导致巩膜变黄。胆红素是血红蛋白的代谢产物，功能不正常时，胆红素无法正常排出，就会在体内聚积。　8、眼部血管斑：患有动脉粥样硬化的患者，一旦在视网膜毛细血管里发现细小的黄色斑块，则说明动脉粥样硬化已经很严重了。　9、视神经异常：在正常情况下，视神经应该呈粉红色，如果颜色变为浅白色，则可能是脑肿瘤、多发性硬化等疾病的征兆。　10、视网膜病变：包括糖尿病、高血压在内的很多疾病都会损伤视网膜上的血管和神经。因此，视网膜渗血、分泌黄色液体、出现白斑等，就应该立即做全身检查。"]
	# htmls = ['<html><body><div class="article-content"><div><p><strong>点击右上角立即关注，更多健康内容不再错过，不定期惊喜送给你</strong></p><p>眼睛既是心灵的窗户，也是人体健康的镜子。通过观察眼部的症状，可以反映出疾病情况，有助于早发现、早治疗，防患于未然。</p><p>　疾病在发生之初，往往都会向人体发出信号，如果不加以重视，就可能会酿成大病。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="447" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057584994371.png"/>　</p><p>1、眼睛充血：眼结膜上布满了毛细血管，一旦血管破裂，就会有充血现象。眼科专家提醒，通常结膜出血没有明显原因，但如果患有严重高血压或血小板缺乏等疾病时，结膜也会充血。</p><p>　2、眼睛凸出：甲亢时甲状腺激素水平异常，会使得眼部周围组织肿胀，眼睛像凸出来一样。</p><p>　3、眼睑下垂：随着年龄增长，多数人会眼睑下垂。但美国加利福尼亚大学眼科临床副教授安德鲁指出，这也可能是脑部肿瘤或者重症肌无力的信号。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="445" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057587182612.png"/>　</p><p>4、瞳孔异常：正常情况下，左右瞳孔应该是对称的。如果瞳孔一大一小或者一侧收缩的速度较慢、幅度较小，就可能是中风、脑肿瘤、视神经肿瘤等疾病的前期症状。</p><p>　5、角膜环：这可能是威尔逊氏病的病症。由于此病患者的铜代谢存在障碍，导致铜沉积角膜上，在瞳孔周围形成一个“角膜环”。</p><p>　6、眼睑增厚：眼睑增厚可能是神经纤维瘤的表现。</p><p>　7、眼球变黄：肝炎和肝硬化等肝功能异常都会引起胆红素积聚，导致巩膜变黄。胆红素是血红蛋白的代谢产物，功能不正常时，胆红素无法正常排出，就会在体内聚积。</p><p>　8、眼部血管斑：患有动脉粥样硬化的患者，一旦在视网膜毛细血管里发现细小的黄色斑块，则说明动脉粥样硬化已经很严重了。</p><p><img alt="疾病时眼睛发出10种信号" img_height="300" img_width="225" inline="0" src="http://article.image.ihaozhuo.com/2017/06/07/14968057589235547.png"/>　</p><p>9、视神经异常：在正常情况下，视神经应该呈粉红色，如果颜色变为浅白色，则可能是脑肿瘤、多发性硬化等疾病的征兆。</p><p>　10、视网膜病变：包括糖尿病、高血压在内的很多疾病都会损伤视网膜上的血管和神经。因此，视网膜渗血、分泌黄色液体、出现白斑等，就应该立即做全身检查。</p></div></div></body></html>']
	filter(id_list, htmls)