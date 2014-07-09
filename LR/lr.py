#!/usr/bin/env python
#author: zuojiepeng
from numpy import *

def LoadData(fname):
	dataMat = []
	labelMat = []
	fr = open(fname, "r")
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat, labelMat

def Sigmoid(z):
	return 1.0 / (1 + exp(-z))

def StocGrandDecent(dataMatIn, classLabels, maxItera, alpha, debug=False):
	dataMatrix = mat(dataMatIn)
	labelMat = mat(classLabels).transpose()
	m, n = shape(dataMatrix)
	weights = ones((n,1))
	for k in range(maxItera):
		dataIdx = range(m) 
		for i in range(m):
			alpha = 4 / (k + i + 1.0) + 0.01
			randIdx = int(random.uniform(0, len(dataIdx)))
			h = Sigmoid(sum(dataMatrix[randIdx] * weights))
			cost = h - labelMat[randIdx]
			weights = weights - alpha * dataMatrix[randIdx].transpose() * cost
			del(dataIdx[randIdx])
	return weights

def GrandDescent(dataMatIn, classLabels, maxItera, alpha, debug=False):
	dataMatrix = mat(dataMatIn)
	labelMat = mat(classLabels).transpose()
	m, n = shape(dataMatrix)
	weights = ones((n, 1))
	for k in range(maxItera):
		h = Sigmoid(dataMatrix * weights)
		cost = (h - labelMat)
		if debug: print str(k) + 'th iteration, cost = ' + str(sum(cost))
		weights = weights - alpha * dataMatrix.transpose() * cost 
	return weights
	
def PlotFitLine(weights, dataMat, labelMat):
	import matplotlib.pyplot as plt 
	m, n = shape(dataMat)
	w = weights.getA()
	for i in range(m):
		if int(labelMat[i]) == 1:
			plt.plot(dataMat[i, 1], dataMat[i,2], 'or')
		elif int(labelMat[i]) == 0:
			plt.plot(dataMat[i, 1], dataMat[i,2], 'ob')
	leftX = min(dataMat[:,1])[0,0]
	rightX = max(dataMat[:,1])[0,0]
	#w[0] * 1 + w[1] * X1 + w[2] * X2 = 0
	leftY = float(-w[0] - w[1] * leftX) / w[2]
	rightY = float(-w[0] - w[1] * rightX) / w[2]
	plt.plot([leftX, rightX], [leftY, rightY], '-g')
	plt.xlabel("X1")
	plt.ylabel("X2")
	plt.show()

def Train():
	alpha = 0.001
	maxItera = 500
	datMat, labelMat = LoadData("data/testSet.txt")
	weights = GrandDescent(datMat, labelMat, maxItera, alpha)
	print weights
	PlotFitLine(weights, mat(datMat), labelMat)

	weights = StocGrandDecent(datMat, labelMat, maxItera, alpha)
	print weights
	PlotFitLine(weights, mat(datMat), labelMat)

if __name__ == "__main__":
	Train()


