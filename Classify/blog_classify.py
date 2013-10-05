#encoding=utf-8
# author: zuojiepeng

import sys
from classify import *
import jieba

jieba.load_userdict("extra_dict/zuojie_dict.txt")
#GNU bash, version 3.2.48(1)-release (x86_64-apple-darwin12)
def Str2Unicode(val, terminal_encode = "utf8"):
	return unicode(val, terminal_encode)

blog_type = {1:"ACM", 2:"IT", 3:"Other"}
rules = {"acm":1, "poj":1, "pku":1, "zoj":1, "zju":1, "hdu":1, "hdoj":1, "noi":1, "解题":1, "icpc":1, "ural":1, "topcoder":1, "codeforces":1, "spoj":1, "uva":1, "邀请赛":1, "模拟赛":1, "赛区":1, "校赛":1, "算法":1, "网赛":1, "网络赛":1, "个人赛":1, "市赛":1, "省赛":1, "题解":1, "水题":1, "judge":1, "php":2, "汇编":2, "单片机":2, "压缩":2, "数据库":2, "测试":2, "android":2, "iphone":2, "ios":2, "mysql":2, "asp":2, "互联网":2, "破解":2, "tomcat":2, "apache":2, "nginx":2, "linux":2, "开发":2, "css":2, "html":2, "javascript":2, "cpp":2, "c++":2, "c#":2, "java":2, "python":2, "ruby":2, "perl":2, "mongodb":2, "oracle":2, "设计":2, "模式":2, "人工智能":2, "机器学习":2, "链接库":2, "系统":2, "架构":2, "编程":2, "visual":2, "程序":2, "教程":2, "入门":2, "编译":2, "数据处理":2}
stop_words = ["", "的", "我", "你", "啊", "the", "个", " ", "原", "转"]

def PreProcess(container):
	if type(container) == dict: 
		tp = {}
		for key, val in container.iteritems():
			if not isinstance(key, unicode): tp[Str2Unicode(key)] = val
			else: tp[key] = val
	elif type(container) == list:
		tp = [Str2Unicode(v) for v in container if not isinstance(v, unicode)] + [v for v in container if isinstance(v, unicode)]
	return tp

#这里可以构造一系列的特征过滤工厂方法XXFilter,过滤特征时按需挨个流水线调用一次,类似lucene里对分词结果的处理
def EncodeFilter(vec):
	return [s for s in vec if isinstance(s, unicode)] + [Str2Unicode(s) for s in vec if not isinstance(s, unicode)]

def StopWordsFilter(vec):
	return [s for s in vec if s not in stop_words]

def LowerFilter(vec):
	return [s.strip().lower() for s in vec]

def GetFeatures(doc):
	splitter = re.compile("\\W*")
	features = [s for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]
	features = LowerFilter(features)
	return dict([(w,1) for w in features])

def GetFeaturesFromBlog(doc):
	features = jieba.cut(doc, cut_all=False)
	features = LowerFilter(features)
	features = EncodeFilter(features)
	features = StopWordsFilter(features)
	return features

def SampleTrain(cf):
	cf.Train("nobody owns the water", "good")
	cf.Train("make quick money at the online casino", "bad")

def ReadDocs(fname):
	docs = [doc.strip() for doc in file(fname)]
	return docs

def RuleBasedTrain(classifier, docs):
	for doc in docs:
		features = GetFeaturesFromBlog(doc)
		classified = False
		for f in features:
			if f in rules.keys():
				classified = True
				print f.encode("utf8"), rules[f]
				classifier.Train(doc, blog_type[rules[f]])
				break
		if classified == False: classifier.Train(doc, blog_type[3])

def LetsRock(fname):
	global rules
	rules = PreProcess(rules)
	docs = ReadDocs("data/blog_title.txt")
	nb = naivebayes(GetFeaturesFromBlog)
	RuleBasedTrain(nb, docs)
	nb.Save(fname)

if __name__ == "__main__":
	training_file = "data/naivebayes_train.dat"
	stop_words = PreProcess(stop_words)
	if len(sys.argv) == 2:
		if sys.argv[1] == "init":
			LetsRock(training_file)
			sys.exit(0)
	docs = ReadDocs("data/final_blog_title.txt")
	#nb = naivebayes(GetFeaturesFromBlog)
	#nb.InitTrainingDat(training_file)
	#for doc in docs: 
	#	print doc + "\t" + nb.Classify(doc)
	fc = fisherclassifier(GetFeaturesFromBlog)
	fc.InitTrainingDat(training_file)
	for doc in docs: 
		print doc + "\t" + fc.Classify(doc)
