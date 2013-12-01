#encoding=utf-8
# author: zuojiepeng

import sys
import jieba
import nmf
from numpy import *

jieba.load_userdict("extra_dict/bili_dict.txt")
bili_blacklist = "./data/blacklist.txt"
stop_words = ["","?", "的", "了"]

def Str2Unicode(val, terminal_encode = "utf-8"):
	return unicode(val, terminal_encode)

def PreProcess(vec):
	if type(vec) == dict:
		tp = {}
		for k, v in vec.iteritems():
			if not isinstance(k, unicode): tp[Str2Unicode(k)] = v
			else: tp[k] = v
	elif type(vec) == list:
		tp = [Str2Unicode(v) for v in vec if not isinstance(v, unicode)] + [v for v in vec if isinstance(v, unicode)]
	return tp

def CutChar(doc):
	features = jieba.cut(doc, cut_all = True)
	return features

def LowerFilter(vec):
	return [s.lower() for s in vec]

def StopWordsFilter(vec):
	return [s for s in vec if s not in stop_words]
	
def EncodeFilter(vec):
	#return [(isinstance(s, unicode) and s or Str2Unicode(s)) for s in vec]
	ss = []
	for s in vec:
		if not isinstance(s, unicode): 
			s = Str2Unicode(s)
		ss.append(s)
	return ss

def GetUserComments():
	users = []
	all_comments = {}
	comments = []
	for line in file(bili_blacklist):
		line = line.strip().strip("\n")
		try:
			user, comment = line.split("|", 2)
		except Exception, e:
			continue
		#print user, comment
		if user not in users:
			users.append(user)
			comments.append({})
		words = CutChar(comment)
		words = EncodeFilter(words)
		words = StopWordsFilter(words)
		words = LowerFilter(words)
		for word in words:
			all_comments.setdefault(word, 0)
			all_comments[word] += 1
			comments[len(comments) - 1].setdefault(word, 0)
			comments[len(comments) - 1][word] += 1
	return comments, all_comments, users

def GetMatrix(all_comments, comments):
	wordvec = []
	for w, c in all_comments.iteritems():
		if c > 3 and c < len(comments) * 0.9:
			wordvec.append(w)
	usr_comment_matrix = [[(word in f and f[word] or 0) for word in wordvec] for f in comments]
	return usr_comment_matrix, wordvec

def Peek(ele, top_k):
	i = 0
	if type(ele) == dict:
		for key, val in ele.iteritems():
			if i > top_k: return
			print key, val
			i += 1
	else: print ele[0:top_k]

def CheckMatrix(comments, usr_comment_matrix, word_vec):
	m, n = len(usr_comment_matrix), len(usr_comment_matrix[0])
	i = 0
	for k, v in comments.iteritems():
		print k + ": ", 
		ele = usr_comment_matrix[i]
		for j in range(len(ele)):
			if ele[j] > 0: print word_vec[j],
		i += 1
		print "\n"

def ShowFeatures(fout, feature_mat, weight_mat, word_vec, users):
	fr, rc = shape(feature_mat)
	top_feature = [[] for i in range(len(users))]
	feature_name = []
	fo = open(fout, "w")
	for i in range(fr):
		fo.write("#" + str(i) + ":")
		slist = []
		for j in range(rc):
			slist.append((feature_mat[i, j], word_vec[j]))
		slist.sort()
		slist.reverse()
		feature_word = [s[1] for s in slist[0:10]]
		for fw in feature_word:
			fo.write(fw.encode("utf8") + ",");
		fo.write("\n")
		# 用第i个特征的前6个关键词代表该特征
		feature_name.append(feature_word)
		flist = []
		for j in range(len(users)):
			flist.append((weight_mat[j, i], users[j]))
			top_feature[j].append((weight_mat[j, i], i))
		flist.sort()
		flist.reverse()
		for f in flist[0:10]:
			fo.write(f[1].decode("utf8").encode("utf8") + " " + str(f[0]) + "\n")
		fo.write("\n")
	fo.close()
	return top_feature, feature_name 

def ShowUserFeature(fout, user_top_feature, feature_name, users):
	fo = open(fout, "w")
	for i in range(len(users)):
		features = user_top_feature[i]
		features.sort()
		features.reverse()
		fo.write(users[i] + ":")
		for j in range(3):
			fo.write("(")
			for fea in feature_name[features[j][1]]:
				fo.write(fea.encode("utf8") + ",")
			fo.write("|" + str(features[j][0]) + "),")
		fo.write("\n")
	fo.close()

# 被拉黑的群体特征无非是：色x、反x、广告、恶意刷屏和其它, 所以规则定为5
def Factorize(mat, features_cnt = 25):
	return nmf.MUR(mat, features_cnt, iters = 60, theta = 0.2)

if __name__ == "__main__":
	stop_words = PreProcess(stop_words)
	comments, all_comments, users = GetUserComments()
	'''
	Peek(comments, 5)
	Peek(all_comments, 5)
	Peek(users, 5)
	'''
	usr_comment_m, word_vec = GetMatrix(all_comments, comments)
	#print usr_comment_m
	#sys.exit(0)
	#Peek(word_vec, 10)
	weight_mat, features_mat = Factorize(usr_comment_m)
	#print usr_comment_m[0:10][0:]
	#CheckMatrix(comments, usr_comment_m, word_vec)
	top_feature, feature_name = ShowFeatures("features.txt", features_mat, weight_mat, word_vec, users) 
	ShowUserFeature("user_feature.txt", top_feature, feature_name, users)
