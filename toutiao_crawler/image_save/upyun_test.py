# coding: utf-8

import upyun
import requests

up = upyun.UpYun('yjk-article-image', 'datag', 'datag123')
up.up_form.endpoint = upyun.ED_AUTO

path = "/2017/06/05/14966432857666666.gif"

url = "http://p1.pstatp.com/large/213900020e048d3d7980"
pic = requests.get(url)

headers = {'x-gmkerl-thumb': '/fw/300'}

up.put(path, pic.content, checksum=True, headers=headers)
