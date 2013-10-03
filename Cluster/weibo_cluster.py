#encoding=utf-8
# author: zuojiepeng
from clusters import *

def Tanimoto(v1, v2):
	c1, c2, shr = 0, 0, 0
	for i in range(len(v1)):
		if v1[i] != 0: c1 += 1
		if v2[i] != 0: c2 += 1
		if v1[i] != 0 and v2[i] != 0: shr += 1
	return 1.0 - (float(shr) / (c1 + c2 - shr))
	#return 1.0 - len(set(v1) & set(v2)) / len(set(v1) | set(v2))

def ReadUserName(fname):
	lines = [line for line in file(fname)]
	name = {}
	for line in lines:
		p = line.strip().split("\t")
		name[p[1]] = p[0]
	return name 

def ReadUserTag(fname):
	lines = [line for line in file(fname)]
	uid = []
	data = []
	for line in lines:
		p = line.strip().split("\t")
		# user has no tag
		if len(p) < 2: continue
		uid.append(p[0])
		data.append(p[1].split(","))
	return uid, data

def ReadMatrix(fname):
	lines = [line for line in file(fname)]
	col_names = lines[0].strip().split("\t")
	row_names = []
	data = []
	for line in lines[1:]:
		p = line.strip().split("\t")
		row_names.append(p[0])
		data.append([float(x) for x in p[1:]])
	return row_names, col_names, data

if __name__ == "__main__":
	#uid, dat = ReadUserTag("data/user_tag_zuojie.txt")
	#user = ReadUserName("data/user_zuojie.txt")
	labels, people, dat = ReadMatrix("data/user_tag_matrix.txt")
	clust = Hcluster(dat, Tanimoto)
	DrawDendrogram(clust, labels, jpeg = "weibo_clusters.jpg")
