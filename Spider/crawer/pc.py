import requests;
import json
import re
from bs4 import  BeautifulSoup
import save
def get_pc_data(url):
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
host="https://m.toutiao.com/list/?tag=news_regimen&ac=wap&count=20&format=json_raw&as=A1C559016B3EFF1&cp=591B9EDFFF61DE1&max_behot_time=1495000323";
result=[]
while True:
    data=get_pc_data(host)
    if data<>"":
     data1=json.loads(data)
     for d in data1["data"]:
         if d["title"] not in result:
             list=[];
             if d.has_key("group_id"):
                 print str(d["group_id"])
                 itemUrl = "http://www.toutiao.com/a"+ str(d["group_id"])
                 r=requests.get(itemUrl)
                 html =r.content
                 soup = BeautifulSoup(html)
                 title = soup.find_all(class_=re.compile("article-title"))[0].text
                 content=soup.find_all(class_=re.compile("article-content"))[0].text
                 # soup_1=soup.find_all(attrs={"class": "article-content"})[0]
                 content=title+"\n"+content
                 print content
             else:
                 content = ""
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
             image_list = str(d["image_list"]) if  d.has_key("image_list") else "";
             result.append(d["title"])
             print group_id, item_id, title, keywords, abstract,source, article_url, display_url, image_list
             list.append([title, keywords, abstract,content,source, article_url, display_url, image_list])
             save.save(list, "qwz")