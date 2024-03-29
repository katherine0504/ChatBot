import requests
import re
import datetime
import pymysql
import saveSightInfo

from bs4 import BeautifulSoup
from bs4 import NavigableString

def openNew(city, url):
	res = requests.get(url)
	print(city)
	bsObj = BeautifulSoup(res.content, "html.parser")

	for obj in bsObj.findAll("ul", {"class":"grid effect-6"}):
		for link in obj.findAll("a", href=re.compile("^(m1)")):
			title = link.div.get_text()
			url = link.attrs['href']
			print(title)
			print(url)
			saveSightInfo.saveInfo(city, title, url)
