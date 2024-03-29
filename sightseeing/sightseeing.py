import requests
import re
import datetime
import pymysql
import urllib
import storeLocation
import saveSightInfo

from bs4 import BeautifulSoup
from bs4 import NavigableString

res = requests.get("http://www.taiwan.net.tw/m1.aspx?sNo=0001016")
bsObj = BeautifulSoup(res.content, "html.parser")

for link in bsObj.find("ul", {"class":"grid effect-6"}).findAll("a", href=re.compile("^(m1)")):
	city = link.div.get_text()
	url = link.attrs['href']
	newUrl = 'http://taiwan.net.tw/' + url
	storeLocation.openNew(city, newUrl)
