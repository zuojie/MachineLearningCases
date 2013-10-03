#encoding=utf-8
# author: zuojiepeng
import urllib2, re
from bs4 import *

cookie = "Your Cookie"
headers = {"cookie":cookie}
zuojiepeng = "http://weibo.com/1805963807/myfollow?t=1&page=%s"
mileyang = "http://weibo.com/p/1005051487394813/follow?relate=fans&page=%s"
user_info = "http://weibo.com/p/10050515%s/info"
user_zuojie = "data/user_zuojie.txt"
user_mile = "data/user_mile.txt"
user_tag_matrix = "data/user_tag_matrix.txt"
user_tag_zuojie = "data/user_tag_zuojie.txt"
p_fans = re.compile(ur"uid=[0-9,]+&fnick=[\u4e00-\u9fa5\-_a-zA-Z0-9]{1,34}&sex=[fm]")
p_following = re.compile(ur"gid=[0-9,]+&nick=[\u4e00-\u9fa5\-_a-zA-Z0-9]{1,34}&uid=[\d]{4,}&sex=[mf]")

def Str2Unicode(val, terminal_encode = "gbk"):
	return unicode(val, terminal_encode)

# 获取粉丝ID
# fans:uid=1307453013&fnick=大太阳在等风来&sex=f urllib
def GetFans(url, fname, pat, cnt):
	f = open(fname, "w")
	users = {}
	pattern = pat
	for i in range(1, cnt + 1):
		page = url % i
		print page
		req = urllib2.Request(page, headers = headers)
		c = urllib2.urlopen(req)
		txt = Str2Unicode(c.read().decode("utf8").encode("gbk", "ignore"))
		ret = pattern.findall(txt)
		for i in ret: 
			#print i
			u = i.split("&")
			nick = u[1].split("=")[1]
			uid = u[0].split("=")[1]
			print nick, uid
			f.write(nick.encode("utf8") + "\t" + uid.encode("utf8") + "\n")
	f.close()

# 获取关注者ID
# following:gid=0&nick=SCatWang&uid=1832563094&sex=m urllib
def GetFollows(url, fname, pat, cnt):
	f = open(fname, "w")
	users = {}
	#pattern = re.compile(ur"gid=[0-9,]+&nick=[\u4e00-\u9fa5\-_a-zA-Z0-9]{1,34}&uid=[\d]{4,}&sex=[mf]")
	pattern = pat
	for i in range(1, cnt + 1):
		page = url % i
		print page
		req = urllib2.Request(page, headers = headers)
		c = urllib2.urlopen(req)
		txt = Str2Unicode(c.read().decode("utf8").encode("gbk"))
		ret = pattern.findall(txt)
		for i in ret: 
			u = i.split("&")
			nick = u[1].split("=")[1]
			uid = u[2].split("=")[1]
			print nick, uid
			f.write(nick.encode("utf8") + "\t" + uid.encode("utf8") + "\n")
	f.close()

# 获取用户标签信息，并写入文件
def GetUserInfo(users):
	url = "http://weibo.com/p/100505%s/info"
	# <span class=\"S_func1\" node-type=\"tag\">美食<\/span>
	pat = re.compile(ur"<span class=\\\"S_func1\\\" node-type=\\\"tag\\\">[\u4e00-\u9fa5\-_a-zA-Z0-9]{1,34}<\\/span>")
	f = open(user_tag_zuojie, "w")
	for uid, name in users.iteritems():
		print uid, name.decode("utf8")
		page = url % uid
		print page
		req = urllib2.Request(page, headers = headers)
		c = urllib2.urlopen(req)
		txt = Str2Unicode(c.read().decode("utf8").encode("utf8"), "utf8")
		ret = pat.findall(txt)
		f.write(uid + "\t")
		first = True
		for i in ret:
			tag = i.split(">")[1].split("<")[0]
			print tag.encode("gbk")
			if first == True: 
				f.write(tag.encode("utf8"))
				first = False
			else: f.write("," + tag.encode("utf8"))
		f.write("\n")
	f.close()

def ReadUserFromFile(fname):
	users = {}
	f = open(fname, "r")
	for line in f.readlines():
		nick, uid = line.strip().split("\t")
		users[uid] = nick
	return users

# 生成用户物品矩阵，适配聚类算法库的输入要求
def GenerateUserTagMatrix(fname):
	users = ReadUserFromFile(user_zuojie)
	user_tag = {}
	tags = set()
	for line in file(user_tag_zuojie):
		line = line.strip()
		print line.decode("utf8")
		dat = line.split("\t")
		uid = dat[0]
		if len(dat) < 2: continue
		utag = dat[1].split(",")
		utag = [u.lower() for u in utag]
		tags = tags | set(utag)
		for t in utag:
			#user_tag[users[uid]].setdefault(t, 1)
			user_tag.setdefault(uid, {})
			user_tag[uid].setdefault(t, 1)
	f = open(fname, "w")
	first = True 
	for t in tags: 
		if first == True: 
			f.write(t)
			first = False
		else: f.write("\t" + t)
	f.write("\n")
	first = True 
	for uid, tag in user_tag.iteritems():
		first = True
		for t in tags: 
			if first == True: 
				f.write(users[uid])
				first = False 
			if t in tag: 
				f.write("\t1") 
			else: 
				f.write("\t0")
		f.write("\n")
	f.close()

def test():
	p = re.compile(ur"gid=0&nick=[\u4e00-\u9fa5_\-a-zA-Z0-9]{4,24}&uid=[\d]{4,}&sex=[mf]")
	txt = Str2Unicode("gid=0&nick=SCatWang&uid=1832563094&sex=m:dsfsds00sdf%dd&gid=0&nick=SCatWang2&uid=1832563094&sex=m")

	#p = re.compile(ur"[\u4e00-\u9fa5_\-a-zA-Z0-9]+")
	#txt = Str2Unicode("哦&abc$23")

	#txt = Str2Unicode("gid=0&nick=徐明明V&uid=1706512355&sex=m")
	ret = p.findall(txt)
	for i in ret: print "### ", i.encode("gbk")

if __name__ == "__main__":
	#GetFollows(zuojiepeng, user_zuojie, p_following, 5)
	#GetFans(mileyang, user_mile, p_fans, 9)
	#users = ReadUserFromFile(user_zuojie)
	#GetUserInfo(users)
	GenerateUserTagMatrix(user_tag_matrix)
