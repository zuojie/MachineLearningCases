#encoding=utf-8
# author: zuojiepeng
import urllib2, re
from bs4 import *

fname = "data/iphone5.dat"
fname_clean = "data/iphone5_clean.dat"

def Str2Unicode(val, terminal_encode = "gbk"):
	return unicode(val, terminal_encode)

def Terminal2Utf8(val, terminal_encode = "gbk"):
	return val.decode(terminal_encode).encode("utf8")

def ParsePage(soup):
	print soup.h1.text#.encoding("gbk")

def GetInfo(fname):
	'''
	url = "http://bj.ganji.com/zq_apple/o%s/"
	pat = re.compile(ur"http:\\/\\/bj.ganji.com\\/shuma\\/[a-zA-Z0-9]{1,10}x.htm")
	'''
	url = "http://www.ganji.com/shoujixinghao/iphone-iphone-5/o%s/"
	f = open(fname, "w")
	for i in range(1, 55):#54
		page = url % i 
		print page
		req = urllib2.Request(page)
		c = urllib2.urlopen(req)
		soup = BeautifulSoup(c.read(), from_encoding="utf-8")
		dls = soup.find_all("dl", attrs={"class", "list_noimg"})
		for dl in dls:
			title = dl.dt.a.text.strip()
			price = dl.dt.span.i.text.strip()
			#print title.encode("gbk", "ignore"), price
			f.write((title + "|" + price + "\n").encode("utf8"))
	f.close()

# clean rule:1,去掉价格单位, 合并标题中所有空格 2，低于1000高于6000的过滤 3，过滤标题中出现仿字的
# 4，将标题字母全部转小写，提取[iphone5，iphone5s，iphone5c, iphone 5, iphone 5s, iphone 5c, 苹果5, 苹果五代, 苹果五, 苹果5c, 苹果5s] 等名字作为特征，合并相似项后，分别用1,2,3表示iphone5，iphone5s，iphone5c，这里标号没有实际意义，只是转化成数值属性方便算法处理。如果提取不到名字信息，按照iphone5处理
# 5，提取颜色信息，黑色为1，白色为2，没有默认3(可以理解为用户1喜欢黑色，用户2喜欢白色，用户3不在乎颜色，这是三种用户类型, 对应着三种不同的定价态度)
# 6，提取闪存大小，直接用作数值属性不再转化。如果没有闪存信息，数据忽略。
# 7，目测二手国行港版价格上并无差别，因此国行/港行属性忽略
def CleanData(fin, fout):
	f = open(fout, "w")
	for line in file(fin):
		line = line.lower()
		line = line.replace(" ", "")
		if Terminal2Utf8("仿") in line: continue
		if "16g" not in line and "32g" not in line and "64g" not in line: continue
		memory = "64"
		if "16g" in line: memory = "16"
		elif "32g" in line: memory = "32"
		title, price = line.split("|")
		price = price.replace(Terminal2Utf8("元"), "")
		if int(price) < 1000 or int(price) > 6000: continue
		version = "1"
		if "iphone5s" in title or Terminal2Utf8("苹果5s") in title: version = "2"
		elif "iphone5c" in title or Terminal2Utf8("苹果5c") in title: version = "3"
		color = "3"
		if Terminal2Utf8("黑色") in title: color = "1"
		elif Terminal2Utf8("白色") in title: color = "2"
		f.write(version + "|" + color + "|" + memory + "|" + price)
		#f.write(title + "|" + price)
	f.close()

def test():
	url = ur"http:\\/\\/bj.ganji.com\\/shuma\\/[a-zA-Z0-9]{1,10}x.htm"
	pat = re.compile(url)
	txt = Str2Unicode('{"url":"http:\/\/bj.ganji.com\/shuma\/698182388x.htm","title":"\u5356\u4e00\u4e2a\u5168\u65b0\u672a\u5f00\u5c01\u7684touch 4\u9ed1\u82728G\u7684","thumb_img":"http:\/\/image.ganjistatic1.com\/gjfs06\/M04\/EF\/79\/wKhxL1JX7duzc,zeAAF532EL25Q375_216-999_8-"')
	ret = pat.findall(txt)
	print ret
	for i in ret: print "### ", i.encode("gbk")
	pass

if __name__ == "__main__":
	#test()
	#GetInfo(fname)
	CleanData(fname, fname_clean)
	#GenerateUserTagMatrix(user_tag_matrix)
