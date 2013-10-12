#encoding=utf-8
# author: zuojiepeng
from optimization import *
from random import random, randint 
import math
from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体  
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题 

def WinePrice(rating, age):
	peak_age = rating - 50
	price = rating / 2
	if age > peak_age:
		price = price * (5 - (age - peak_age))
	else:
		price = price * (5 * ((age + 1) / peak_age))
	if price < 0: price = 0
	return price

def WineSet2():
	rows = WineSet1()
	for row in rows:
		if random() < 0.5: row["result"] *= 0.5
	return rows

def WineSet1():
	rows = []
	for i in range(300):
		rating = random() * 50 + 50
		age = random() * 50
		price = WinePrice(rating, age)
		price *= (random() * 0.4 + 0.8)
		rows.append({"input":(rating, age, aisle, bottle_size), "result":price})
	return rows

def WineSet():
	rows = []
	for i in range(300):
		rating = random() * 50 + 50
		age = random() * 50
		aisle = float(randint(1, 20))
		bottle_size = [375.0, 375.0, 1500.0, 3000.0][randint(0, 3)]
		price = WinePrice(rating, age)
		price *= bottle_size / 750
		price *= (random() * 0.9 + 0.2)
		rows.append({"input":(rating, age, aisle, bottle_size), "result":price})
	return rows

def Euclidean(v1, v2):
	return math.sqrt(sum([(v1[i] - v2[i]) ** 2 for i in range(len(v1))]))

def GetDistances(data, v):
	distances = [(Euclidean(v, data[i]["input"]), i) for i in range(len(data))]
	distances.sort()
	return distances

def KnnEstimate(data, v, k = 5):
	distances = GetDistances(data, v)
	if k > len(distances): k = len(distances)
	return sum([data[distances[i][1]]["result"] for i in range(k)]) / k

def CreateCostFunction(AlgF, data):
	def CostF(scale):
		sdata = ReScale(data ,scale)
		return CrossValidate(AlgF, sdata, trials = 10)
	return CostF

def InverseWeight(dist, num = 1.0, const = 0.1):
	return num / (dist + const)

def SubractWeight(dist, const = 1.0):
	if dist > const: return 0
	return const - dist

def Gaussian(dist, sigma = 10.0):
	return math.e ** (-dist ** 2 / (2 * sigma ** 2))

def WeightedKnn(data, v, k = 5, WeightF = Gaussian):
	distances = GetDistances(data, v)
	if k > len(distances): k = len(distances)
	res = [(data[distances[i][1]]["result"], WeightF(distances[i][0])) for i in range(k)]
	avg, tot = zip(*res)
	avg = map(lambda x,y:x*y, avg, tot)
	return sum(avg) / sum(tot)

def DivideData(data, test = 0.05):
	test_set = [dat for dat in data if random() < test]
	train_set = [dat for dat in data if dat not in test_set]
	return train_set, test_set

def TestAlgorithm(AlgF, train_set, test_set):
	return sum([(row["result"] - AlgF(train_set, row["input"])) ** 2 for row in test_set]) / len(test_set)

def CrossValidate(AlgF, data, trials = 100, test = 0.05):
	error = 0.0
	for i in range(trials):
		train_set, test_set = DivideData(data, test)
		error += TestAlgorithm(AlgF, train_set, test_set)
	return error / trials

def KnnInverse(d, v):
	return WeightedKnn(d, v, WeightF = InverseWeight)

def ReScale(data, scale):
	return [{"input":[scale[i] * row["input"][i] for i in range(len(scale))], "result":row["result"]} for row in data]

def ProbGuess(data, vec, low, high, k = 5, WeightF = Gaussian):
	distances = GetDistances(data, vec)
	nweight = 0
	tweight = 0
	for i in range(k):
		dist = distances[i][0]
		idx = distances[i][1]
		weight = WeightF(dist)
		v = data[idx]["result"]
		if v >= low and v <= high: nweight += weight
		tweight += weight
	if tweight == 0: return 0
	return nweight / tweight

def CumulativeGraph(data, vec, high, step = 0.1, k = 5, WeightF = Gaussian):
	x = arange(0.0, high, step)
	y = array([ProbGuess(data, vec, 0, v, k, WeightF) for v in x])
	plot(x, y, "ro-")
	show()

def ProbabilityGraph(data, vec, high, step = 0.1, k = 5, WeightF = Gaussian, ss = 5.0):
	x = arange(0.0, high, step)
	probs = [ProbGuess(data, vec, v, v + 0.1, k, WeightF) for v in x]
	smoothed = []
	for i in range(len(probs)):
		sv = 0.0
		for j in range(0, len(probs)):
			dist = abs(i - j) * 0.1
			weight = Gaussian(dist, sigma = ss)
			sv += weight * probs[j] 
		smoothed.append(sv)
	y = array(smoothed)
	plot(x, y, "ro-")
	show()

if __name__ == "__main__":
	data = WineSet()
	print Euclidean(data[0]["input"], data[1]["input"])
	print KnnEstimate(data, (95.0, 5.0))
	print WeightedKnn(data, (95.0, 5.0))
	print WinePrice(95.0, 5.0)
	'''
	print CrossValidate(KnnEstimate, data)
	print CrossValidate(Knn3, data)
	print CrossValidate(KnnInverse, data)
	'''
	print ProbGuess(data, [99, 20], 40, 80)
	print ProbGuess(data, [99, 20], 120, 1000)
	print ProbGuess(data, [99, 20], 30, 120)
	#CumulativeGraph(data, (1,1), 120)
	ProbabilityGraph(data, (1,1), 120)
	'''
	CostF = CreateCostFunction(KnnEstimate, data)
	weight_domain = [(0, 20)] * 4
	scale  = AnnealingOptimize(weight_domain, CostF, step = 2)
	#scale  = GeneticOptimize(weight_domain, CostF, pop_seize = 5, step = 2)
	print scale
	data = ReScale(data, [10, 10, 0, 0.5])
	print CrossValidate(KnnEstimate, data)
	print CrossValidate(Knn3, data)
	print CrossValidate(KnnInverse, data)
	'''
