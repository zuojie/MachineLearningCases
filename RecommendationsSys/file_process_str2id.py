#encoding=utf-8
import sys

path = "data/"
fname_item_out = path + "dianping_huoguo_itemid.txt"
fname_item_addr_out = path + "dianping_huoguo_addr_itemid.txt"
fname_user_out = path + "dianping_huoguo_userid.txt"
fname_user_trans_out = path + "dianping_huoguo_userid_based.txt"
fname_user_addr_trans_out = path + "dianping_huoguo_userid_addr_based.txt"
fname_item_in = path + "dianping_huoguo_item_based.txt"
fname_user_in = path + "dianping_huoguo_user_based.txt"
fname_user_addr_in = path + "dianping_huoguo_user_addr_based.txt"

def Name2ID(fin, item = True):
	if item: 
		#fout = fname_item_out
		fout = fname_item_addr_out
		separator = ":"
	else:
		fout = fname_user_out
		separator = "|"
	fo = open(fout, "w")
	i = 1
	dic_tp = {}
	for line in file(fin):
		name = line.split(separator)[0]
		# È¥³ýµêÖ·ÐÅÏ¢
		#if item: name = name.split("(")[0]
		if name in dic_tp: continue
		dic_tp.setdefault(name, 0)
		fo.write(str(i) + "\t" + name)
		fo.write("\n")
		i += 1
	fo.close()

def TransData(fout = fname_user_trans_out):
	user = {}
	item = {}
	for line in file(fname_user_out):
		line = line.strip("\n")
		id, name = line.split("\t")
		user[name] = id 
	#for line in file(fname_item_out):
	for line in file(fname_item_addr_out):
		line = line.strip("\n")
		id, name = line.split("\t")
		item[name] = id 
	fo = open(fout, "w")
	#for line in file(fname_user_in):
	for line in file(fname_user_addr_in):
		name, shop = line.split("|")
		val = user[name] + "\t" 
		shops = shop.split(",")
		for i in shops:
			name, score = i.split(":")
			score = score.strip("\n")
			try:
				fo.write(val + item[name] + "\t" + score + "\n")
			except KeyError:
				print name.decode("utf-8", "ignore")
				continue
	fo.close()

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "no file!"
		sys.exit(0)
	Name2ID(fname_item_in)
	#Name2ID(fname_user_in, False)
	#TransData()
	TransData(fname_user_addr_trans_out)
	sys.exit(0)
