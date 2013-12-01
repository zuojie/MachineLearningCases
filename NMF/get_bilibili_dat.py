#encoding=utf-8
# author: zuojie peng
import urllib2
from bs4 import *

bili = "http://www.bilibili.tv/account/badlist.html"
bili_html = "bili.html"
bili_tbl = "./data/badlist.table"

def PrintUTF8Terminal(val):
	return val.encode("utf-8", "ignore")

def GetBadList(outf):
	#req = urllib2.Request(url = bili)
	#c = urllib2.urlopen(req)
	#soup = BeautifulSoup(c.read(), from_encoding="utf-8")
	#soup = BeautifulSoup(c.read())
	'''
	f = file(bili_html)
	soup = BeautifulSoup(f, from_encoding="utf-8")
	table = soup.find_all("table", attrs={"class", "badlist"})
	table = str(table[0])
	f = open("badlist.table", "w")
	f.write(table)
	f.close()
	'''
	table = file(bili_tbl)
	soup = BeautifulSoup(table)
	trs = soup.find_all("tr")
	trs = trs[1:]
	f = open("blacklist.txt", "w")
	for tr in trs:
		tds = tr.find_all("td")
		user = tds[1].text.strip()
		msg = tds[5]
		try:
			msg.b.clear()
			msg = tds[5].text.strip()
		except Exception, e:
			msg = tds[5].text.strip()
			msg = msg.strip("Tag:").strip()
			pass
		#print user, msg
		out_str = user + "|" + msg  
		out_str = out_str.encode("utf-8")
		f.write(out_str + "\n")
	f.close()

if __name__ == "__main__":
	GetBadList("bilibili.badlist")

