<<<<<<< HEAD
import pytz

from datetime import datetime
tz = pytz.timezone('Asia/Shanghai')
print(datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S'))
=======
import requests
from bs4 import BeautifulSoup

a = "2017-05-04 19:55:00"
b = "2017-07-03 23:46"

print(len(a))
print(len(b))
>>>>>>> 0a1ae33549bcf4af396c1e0e4a209df409c45687
