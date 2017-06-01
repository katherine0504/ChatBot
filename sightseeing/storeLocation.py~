import requests
import re
import datetime
import pymysql
import saveSightInfo

from bs4 import BeautifulSoup
from bs4 import NavigableString

def openNew(city, url):
	res = requests.get(url)
	print(res.encoding)
	print(city)
	bsObj = BeautifulSoup(res.content, "html.parser")

	for link in bsObj.find("ul", {"class":"grid effect-6"}).findAll("a", href=re.compile("^(m1)")):
		title = link.div.get_text()
		url = link.attrs['href']
		print(title)
		print(url)
		saveSightInfo.saveInfo(city, title, url)
