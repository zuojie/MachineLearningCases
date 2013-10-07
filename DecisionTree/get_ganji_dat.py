#encoding=utf-8
# author: zuojiepeng
import urllib2, re
import traceback
from bs4 import *

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}
#296 pages total
rent_hourse = "http://bj.ganji.com/fang1/o%s/"

def Encode(val, codec = "gbk"):
	return val.encode(codec, "ignore")

def ParsePage(soup, f):
		divs = soup.find_all("dl", attrs={"class", "list-img"})
		for div in divs:
			try:
				list_word = div.find_all("p", attrs={"class", "list-word"})
				addrs = list_word[0].find_all("span", attrs={"class", "list-word-col"})
				if len(addrs) == 1: address = addrs[0].a.text
				elif len(addrs) == 2: address = addrs[1].a.text
				else: print addrs
				info = list_word[1].text
				info_f = Encode(info, "utf8")
				info = info.split("/")
				rooms = info[0]
				space = info[1]
				if len(info) == 7:
					fitment = info[2]
					floor = info[3]
					direction = info[5]
				else:
					fitment = "None"
					floor = info[2]
					direction = info[4]
				price = div.find("span", attrs={"class", "price"})
				price_number = price.b.text
				f.write(info_f + "\n")
				f.write(Encode(address, "utf8") + "\t" 
						+ Encode(rooms, "utf8") + "\t"
						+ Encode(space, "utf8") + "\t" 
						+ Encode(fitment, "utf8") + "\t" 
						+ Encode(floor, "utf8") + "\t" 
						+ Encode(direction, "utf8") + "\t" 
						+ Encode(price_number, "utf8") + "\n")
			except Exception, e:
				msg = traceback.format_exc()
				print msg
				continue

def Crawl(url, fname):
	total = 297
	f = open(fname, "w")
	for i in range(201, total):
		page = url % i
		print page
		try:
			req = urllib2.Request(url = page,
					headers = headers)
			c = urllib2.urlopen(req, timeout=15)
			soup = BeautifulSoup(c.read(), from_encoding="utf-8")
			ParsePage(soup, f)
		except Exception, e:
			msg = traceback.format_exc()
			print msg
			continue
	f.close()
		
def PreProcess(fin, fout):
	fo = open(fout, "w")
	i = 1
	for line in file(fin):
		if "/" not in line:
			line = line.strip()
			line = line.replace("„é°", "")
			direction = unicode("œÚ", "gbk")
			rooms = unicode(" “", "gbk")
			price = unicode("√Ê“È", "gbk")
			if (direction in line.decode("utf-8", "ignore")) and (price not in line.decode("utf-8", "ignore")): 
				if rooms in line.decode("utf-8", "ignore"): fo.write(line + "\n")
			else: print "shoot!"
		else: continue
	fo.close()

if __name__ == "__main__":
	fin = "data/rent_house.dat"
	#Crawl(rent_hourse, fin)
	fout = "data/rent_house_clean.dat"
	PreProcess(fin, fout)
