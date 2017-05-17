#!/usr/local/bin/python2.7
# -*- coding: utf8 -*-
"""  
  超级课程表话题抓取  
"""
import urllib2
import requests;
from cookielib import CookieJar
import json
from bs4 import BeautifulSoup
import save

''' 读Json数据 '''

# def fetch_data(json_data):
#     data = json_data['data']
#     timestampLong = data['timestampLong']
#     messageBO = data['messageBOs']
#     topicList = []
#     for each in messageBO:
#         topicDict = {}
#         if each.get('content', False):
#             topicDict['content'] = each['content']
#             topicDict['schoolName'] = each['schoolName']
#             topicDict['messageId'] = each['messageId']
#             topicDict['gender'] = each['studentBO']['gender']
#             topicDict['time'] = each['issueTime']
#             print each['schoolName'], each['content']
#             topicList.append(topicDict)
#     return timestampLong, topicList
#
#
# ''' 加载更多 '''


# def load(timestamp, headers, url):
#     headers['Content-Length'] = '159'
#     loadData = 'timestamp=%s&phoneBrand=Meizu&platform=1&genderType=-1&topicId=19&phoneVersion=16&selectType=3&channel=MXMarket&phoneModel=M040&versionNumber=7.2.1&' % timestamp
#     req = urllib2.Request(url, loadData, headers)
#     loadResult = opener.open(req).read()
#     loginStatus = json.loads(loadResult).get('status', False)
#     if loginStatus == 1:
#         print 'load successful!'
#         timestamp, topicList = fetch_data(json.loads(loadResult))
#         load(timestamp, headers, url)
#     else:
#         print 'load fail'
#         print loadResult
#         return False



# loginUrl = 'http://120.55.151.61/V2/StudentSkip/loginCheckV4.action'
# topicUrl = 'http://120.55.151.61/V2/Treehole/Message/getMessageByTopicIdV3.action'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'News/6.1.2 (iPhone; iOS 9.3.5; Scale/2.00)',
    'Host': 'lf.snssdk.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
    'Content-Length': '207',
    'Accept-Language': 'zh-Hans-CN'
}

''' ---登录部分--- '''
topicUrl = 'http://lf.snssdk.com/api/news/feed/v53/?version_code=6.1.2&app_name=news_article&vid=2DCC55A3-86D2-4085-8305-DE9A10B98A0A&device_id=35984383313&channel=App%20Store&resolution=750*1334&aid=13&ab_version=124684,126063,125849,127422,114038,122834,126066,125865,123726,114104,127194,127126,126069,126788,125503,125174,127336,126058,127379,126470,126526,126303,122948,127222,123126,31648,126990,121007,126020,114338&ab_feature=z1&openudid=21621ef2fc3977021be869c1fdd5dbad1098ff3b&live_sdk_version=1.6.5&idfv=2DCC55A3-86D2-4085-8305-DE9A10B98A0A&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=10265724514&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=E0DA105A-6C57-4245-AEE6-6D7D898BDF44&LBS_status=authroize&category=news_health&city=%E6%9D%AD%E5%B7%9E&concern_id=6215497895248923137&count=20&cp=549e17A7Ab529q1&detail=1&image=1&language=zh-Hans-CN&last_refresh_sub_entrance_interval=19303&latitude=30.28361140797248&loc_mode=1&loc_time=1494917136&longitude=120.010757944166&min_behot_time=1494901846&refer=1&strict=0&tt_from=click_tip'
text1Url = "http://lf.snssdk.com/article/content/16/2/"
text2Url = "/1/?version_code=6.1.2&app_name=news_article&vid=2DCC55A3-86D2-4085-8305-DE9A10B98A0A&device_id=35984383313&channel=App%20Store&resolution=750*1334&aid=13&ab_version=124684,126063,125849,127422,114038,122834,126066,125865,123726,114104,127194,127126,126069,126788,125503,125174,127336,126058,127379,126470,126526,126303,122948,127222,123126,31648,126990,121007,126020,114338&ab_feature=z1&openudid=21621ef2fc3977021be869c1fdd5dbad1098ff3b&live_sdk_version=1.6.5&idfv=2DCC55A3-86D2-4085-8305-DE9A10B98A0A&ac=WIFI&os_version=9.3.5&ssmix=a&device_platform=iphone&iid=10265724514&ab_client=a1,f2,f7,e1&device_type=iPhone%206S&idfa=E0DA105A-6C57-4245-AEE6-6D7D898BDF44"
testUrl = "https://lf.snssdk.com/api/news/feed/v53/?category=news_health&concern_id=6215497895248923137&refer=1&count=20&min_behot_time=&last_refresh_sub_entrance_interval=&loc_mode=0&tt_from=enter_auto&cp=569419a4d874dq1&iid=10291744168&device_id=36372853508&ac=wifi&channel=xiaomi&aid=13&app_name=news_article&version_code=612&version_name=6.1.2&device_platform=android&ab_version=125481%2C124685%2C126064%2C124993%2C125842%2C127421%2C126035%2C114040%2C122834%2C126065%2C125865%2C123727%2C127188%2C127130%2C126071%2C125839%2C126791%2C125503%2C125174%2C127527%2C127333%2C104321%2C126058%2C127138%2C126401%2C126526%2C126125%2C122948%2C123125%2C31244%2C127080%2C126153%2C121011%2C125527%2C126014%2C114338%2C127485%2C125065&ab_client=a1%2Cc4%2Ce1%2Cf2%2Cg2%2Cf7&ab_feature=94563%2C102749&abflag=3&ssmix=a&device_type=Redmi+Note+4&device_brand=Xiaomi&language=zh&os_api=23&os_version=6.0&uuid=862963032864841&openudid=c7ef43d7c65a8f17&manifest_version_code=612&resolution=1080*1920&dpi=480&update_version_code=6124&_rticket="

cookieJar = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
opener.addheaders = [('User-Agent', 'News/6.1.2 (iPhone; iOS 9.3.5; Scale/2.00)')];
opener.addheaders.append(('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'))
opener.addheaders.append(('Host', 'lf.snssdk.com'))
opener.addheaders.append(('Connection', 'Keep-Alive'))
# opener.addheaders.append(('Accept-Encoding','gzip'))
opener.addheaders.append(('Accept-Language', 'zh-Hans-CN'))
result=[]
while True:
    result1 = opener.open(testUrl)
    data1 = result1.read()
    json_data = json.loads(data1)
    json_result = json_data["data"]
    for json_content in json_result:
        if  json.loads(json_content["content"]).has_key("tag_id"):
            tag_id = json.loads(json_content["content"])["tag_id"]
            itemUrl = text1Url + str(json.loads(json_content["content"])["tag_id"]) + "/" + str(
                json.loads(json_content["content"])["item_id"]) + text2Url
            result2 = opener.open(itemUrl)
            data2 = result2.read()
            html = json.loads(data2)["data"]["content"]
            soup = BeautifulSoup(html)
            content = soup.text
        else:
            content = ""
            tag_id = "";
        group_id = json.loads(json_content["content"])["group_id"] if json.loads(json_content["content"]).has_key(
            "group_id") else "";
        item_id = json.loads(json_content["content"])["item_id"] if json.loads(json_content["content"]).has_key(
            "item_id") else "";
        title = json.loads(json_content["content"])["title"] if json.loads(json_content["content"]).has_key(
            "title") else "";
        keywords = json.loads(json_content["content"])["keywords"] if json.loads(json_content["content"]).has_key(
            "keywords") else "";
        abstract = json.loads(json_content["content"])["abstract"] if json.loads(json_content["content"]).has_key(
            "abstract") else "";
        source = json.loads(json_content["content"])["source"] if json.loads(json_content["content"]).has_key(
            "source") else "";
        article_url = json.loads(json_content["content"])["article_url"] if json.loads(json_content["content"]).has_key(
            "article_url") else "";
        display_url = json.loads(json_content["content"])["display_url"] if json.loads(json_content["content"]).has_key(
            "display_url") else "";
        image_list = str(json.loads(json_content["content"])["image_list"] )if json.loads(json_content["content"]).has_key(
            "image_list") else "";
        print tag_id, group_id, item_id, title, keywords, abstract, content, source, article_url, display_url, image_list
        content_list=[title, keywords, abstract, content, source, article_url, display_url, image_list]
        result_list = []
        if content_list not in result:
            result.append(content_list)
            result_list.append(content_list)
        save.save(result_list, "qwz")




        # jsonresult=json.loads(datas)
        # data=jsonresult['data']
        # print data["content"]
        # for d in data:
        #     print d
        #     dd=d["content"]
        #     ddd=json.loads(dd)
        #     print ddd["title"]

        # ''' ---获取话题--- '''
        # topicData = 'timestamp=0&phoneBrand=Meizu&platform=1&genderType=-1&topicId=19&phoneVersion=16&selectType=3&channel=MXMarket&phoneModel=M040&versionNumber=7.2.1&'
        # headers['Content-Length'] = '147'
        # topicRequest = urllib2.Request(topicUrl, topicData, headers)
        # topicHtml = opener.open(topicRequest).read()
        # topicJson = json.loads(topicHtml)
        # topicStatus = topicJson.get('status', False)
        # print topicJson
        # if topicStatus == 1:
        #     print 'fetch topic success!'
        #     timestamp, topicList = fetch_data(topicJson)
        #     load(timestamp, headers, topicUrl)
