#encoding=utf-8
# author: zuojiepeng
from numpredict import *

def GetData(fname):
	rows = []
	for line in file(fname):
		line = line.strip()
		version, color, memory, price = line.split("|")
		rows.append({"input":(float(version), float(color), float(memory)), "result":float(price)})
	return rows

if __name__ == "__main__":
	# iphone5 16g
	vec = [1, 3, 16]
	data = GetData("data/iphone5_clean.dat")
	prices = [dat["result"] for dat in data]
	min_price = min(prices)
	max_price = max(prices)
	print "Min Price: " + str(min_price) 
	print "Max Price: " + str(max_price)

	# KNN进行价格预估
	print KnnEstimate(data, vec)
	print WeightedKnn(data, vec)

	# 交叉验证裸knn和加权knn的预测优劣
	#print CrossValidate(KnnEstimate, data)
	#print CrossValidate(WeightedKnn, data)

	# 绘制累计概率分布图
	#CumulativeGraph(data, vec, max_price, step = 10, k = 10)
	# 绘制价格概率分布图
	#ProbabilityGraph(data, vec, max_price, step = 10, k = 10)

	# 通过优化算法寻找最佳缩放向量
	'''
	weight_domain = [(1, 10), (1, 10), (1, 2)]
	CostF = CreateCostFunction(KnnEstimate, data)
	scale = AnnealingOptimize(weight_domain, CostF, step = 2)
	print scale
	'''
	# 模拟退火太慢，计算出缩放因子后写死在代码中
	scale = [6, 1, 1]
	# 归一化数据集，将对定价影响不同的属性值进行相应缩放
	sdata = ReScale(data, scale)
	vec = map(lambda x,y:x*y, vec, scale)
	print data[0]
	print sdata[0]
	# KNN进行价格预估
	print KnnEstimate(sdata, vec)
	print WeightedKnn(data, vec)
	# 绘制累计概率分布图
	CumulativeGraph(sdata, vec, max_price, step = 10, k = 10)
	# 绘制价格概率分布图
	ProbabilityGraph(sdata, vec, max_price, step = 10, k = 10)

