import requests
import re
import datetime
import pymysql
import json
import urllib.parse

from bs4 import BeautifulSoup
from bs4 import NavigableString
from pymongo import MongoClient, errors

uri = "mongodb://kathy:kathy@ds141960.mlab.com:41960/kathytest"
client = MongoClient(uri)
db = client.kathytest
collect = db.travel

def store(obj):
	collect.insert_one(obj)

def saveInfo(city, title, url):
	url = 'http://taiwan.net.tw/' + url
	res = requests.get(url)
	bsObj = BeautifulSoup(res.content, "html.parser")
	title = bsObj.select(".attractionsLeft h1")
	title = ''.join(str(e) for e in title)
	title = title.replace("<h1>", "").replace("</h1>", "").replace(" ", "").replace("\r\n", "")
	info = bsObj.select(".attractionsLeft p")
	info = ''.join(str(e) for e in info)
	info = info.replace("<p>", "").replace("</p>", "")
	print(info)
	details = bsObj.select(".attractionsDl dd")
	recommend = bsObj.select(".RecommendNumber")
	rec = ''.join(str(e) for e in recommend)
	recommend = re.sub('<[^>]*>', '', rec)
	obj = {
		'city': city,
		'name': title,
		'url': url,
		'info': info,
		'phone': '',
		'address': '',
		'geo': '',
		'web': '',
		'drive': '',
		'trans': '',
		'recommend': recommend
  }
	cnt = 0
	for dd in details:
		cnt = cnt +1
		if (cnt == 1) :
			phone = str(dd)
			phone = phone.replace("<dd>", "").replace("</dd>", "")
			obj['phone'] = phone

		elif (cnt == 2):
			address = str(dd)
			address = address.replace("<dd>", "").replace("</dd>", "")
			obj['address'] = address

		elif (cnt == 3):
			geo = str(dd)
			geo = geo.replace("<dd>", "").replace("</dd>", "")
			obj['geo'] = geo

		elif (cnt == 4):
			web = str(dd)
			web = web.replace("<dd>", "").replace("</dd>", "")
			p = re.compile(r'<.*?>')
			web = p.sub('', web)
			obj['web'] = web

		elif (cnt == 5):
			drive = str(dd)
			drive = drive.replace("<dd>", "").replace("</dd>", "").replace("<p>", ""). replace("</p>", "")
			obj['drive'] = drive

		elif (cnt == 6):
			trans = str(dd)
			trans = trans.replace("<dd>", "").replace("</dd>", "").replace("<p>", "").replace("</p>", "").replace("<br>", "").replace("<br/>", "")
			obj['trans'] = trans
	store(obj)


