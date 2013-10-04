#encoding=utf-8
# author: zuojiepeng

from classify import *

#这里可以构造一系列的特征过滤工厂方法XXFilter,过滤特征时按需挨个流水线调用一次,类似lucene里对分词结果的处理
def LowerFilter(vec):
	return [s.lower() for s in vec]

def GetFeatures(doc):
	splitter = re.compile("\\W*")
	features = [s for s in splitter.split(doc) if len(s) > 2 and len(s) < 20]
	features = LowerFilter(features)
	return dict([(w,1) for w in features])

def SampleTrain(cf):
	cf.Train("nobody owns the water", "good")
	cf.Train("the quick brown fox jumps over the lazy dog", "good")
	cf.Train("the quick rabbit jumps fence", "good")
	cf.Train("buy pharmaceuticals now", "bad")
	cf.Train("the quick learning, coursea", "bad")
	cf.Train("make quick money at the online casino", "bad")

if __name__ == "__main__":
	'''
	cf = classifier(GetFeatures)
	SampleTrain(cf)
	print cf.FeatureCnt("quick", "good")
	print cf.FProb("quick", "good")
	print cf.WeightedProb("money", "good", cf.FProb)
	SampleTrain(cf)
	print cf.WeightedProb("money", "good", cf.FProb)
	'''

	'''
	nb = naivebayes(GetFeatures)
	SampleTrain(nb)
	print nb.BayesProb("quick rabbit", "good")
	print nb.BayesProb("quick rabbit", "bad")
	print ""
	print nb.Classify("quick money")
	print ""
	nb.SetThreshold("bad", 3.0)
	print nb.Classify("quick money")
	print ""
	for i in range (10): SampleTrain(nb)
	print nb.Classify("quick money")
	'''

	fc = fisherclassifier(GetFeatures)
	SampleTrain(fc)
	print fc.CProp("quick", "good")
	print fc.CProp("money", "bad")
	print fc.WeightedProb("money", "bad", fc.CProp)
	print fc.FisherProb("quick rabbit", "good")
	print fc.FisherProb("quick rabbit", "bad")
	print fc.Classify("quick rabbit")
	print fc.Classify("quick money")
	fc.SetCritical("bad", "0.8")
	print fc.Classify("quick money")
	fc.SetCritical("good", "0.4")
	print fc.Classify("quick money")
