# coding: utf-8
"""
Crawl medical news from Toutiao pc web.

Version: Python 2.7
Author: Huang Jinbao, He Youqiang
Date: 20170520
"""

import json
import random
import re
import time
import requests
from bs4 import BeautifulSoup
import save


def download(url):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, sdch, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Host': 'm.toutiao.com',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36'
               }
    r = requests.get(url, headers=headers)
    return r.content

def spider():
    host = "https://m.toutiao.com/list/?tag=news_regimen&ac=wap&count=20&format=json_raw&as=A1C559016B3EFF1&cp=591B9EDFFF61DE1&max_behot_time=1495000323";
    result = []
    i = 0
    png={}
    while True:
        try:
            data = download(host)
            if data <> "":
                data1 = json.loads(data)
                for d in data1["data"]:
                    if d["title"] not in result:
                        list = [];
                        if d.has_key("group_id"):
                            itemUrl = "http://www.toutiao.com/a" + str(d["group_id"])
                            try:
                                r = requests.get(itemUrl)
                                html = r.content
                                soup = BeautifulSoup(html)
                                pstr=""
                                create_time = soup.find_all(class_="time")[0].text
                                if len(soup.find_all(id="article-main"))>0:
                                    for pp in soup.find_all(id="article-main")[0].find_all("p"):
                                         pstr+="\n"+str(pp)
                                         if len(pp.find_all("img"))>0:
                                             url=pp.find_all("img")[0]["src"]
                                             r=requests.get(url)
                                             img=[]
                                             img.append([url,r.content])
                                             # time.sleep(random.random() * 10)
                                             save.save_img(img, "toutiao_pc_img")
                                             # png[url]=r.content
                                             # file="d://test//"+str(i+1)+".png"
                                             # print file
                                             # f = open(file, 'wb')
                                             # f.write(r.content)
                                             # f.close()
                                    title = soup.find_all(class_=re.compile("article-title"))[0].text
                                    content = soup.find_all(class_=re.compile("article-content"))[0].text
                                    # soup_1=soup.find_all(attrs={"class": "article-content"})[0]
                                    content = title + "\n" + content
                                    contents=pstr

                                    group_id = d["group_id"] if d.has_key(
                                        "group_id") else "";
                                    item_id = d["item_id"] if d.has_key(
                                        "item_id") else "";
                                    title = d["title"] if d.has_key(
                                        "title") else "";
                                    keywords = d["keywords"] if d.has_key(
                                        "keywords") else "";
                                    abstract = d["abstract"] if d.has_key(
                                        "abstract") else "";
                                    source = d["source"] if d.has_key(
                                        "source") else "";
                                    article_url = d["article_url"] if d.has_key(
                                        "article_url") else "";
                                    display_url = d["display_url"] if d.has_key(
                                        "display_url") else "";
                                    image_list = str(d["image_list"]) if d.has_key("image_list") else "";
                                    result.append(d["title"])
                                    list.append([title, keywords, abstract, content, source, article_url, display_url, image_list,contents,create_time])
                                    i += 1
                                    print "目前正在采集第" + str(i) + "条数据"
                                    save.save_text(list, "toutiao_pc")
                                    interval = random.randint(100, 150)
                                    if (i % interval == 0):
                                        time.sleep(random.random() * 1000)
                            except:
                                continue
        except:
            continue
