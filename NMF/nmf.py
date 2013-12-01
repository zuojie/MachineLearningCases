#encoding=utf-8
# author: zuojiepeng

from numpy import *

# 估价函数
def CostF(current, target):
	dif = 0
	m, n = shape(current)
	for i in range(m):
		for j in range(n):
			dif += pow(current[i, j] - target[i, j], 2)
	return dif

# multiplicative update rules
def MUR(mat, features = 10, iters = 50, theta = 0.2, threshold = 5e-6):
	mat = matrix(mat)
	ic, fc = shape(mat)
	#print ic, fc
	weight_mat = matrix([[random.random() for j in range(features)] for i in range(ic)])
	feature_mat = matrix([[random.random() for i in range(fc)] for i in range(features)])
	for i in range(iters):
		wf = weight_mat * feature_mat
		cost = CostF(wf, mat)
		cost = sqrt(cost)
		if i % 10 == 0: print cost
		if cost == 0: 
			break
		if i > 0 and abs(last_cost - cost) < threshold:
			print abs(last_cost - cost), threshold
			break
		last_cost = cost

		'''
		print i, "weight_mat.T: ", weight_mat.T
		print i, "weight_mat: ", weight_mat
		print i, "feature_mat: ", feature_mat 
		print i, "mat: ", mat 
		'''

		# 更新特征矩阵
		feature_n = weight_mat.T * mat
		feature_d = weight_mat.T * weight_mat * feature_mat
		#feature_mat = matrix((array(feature_mat) * array(feature_n) + theta) / (array(feature_d) + theta))	
		feature_mat = matrix(array(feature_mat) * array(feature_n) / (array(feature_d) + theta))	
		# 更新权重矩阵
		weight_n = mat * feature_mat.T
		weight_d = weight_mat * feature_mat * feature_mat.T
		weight_mat = matrix(array(weight_mat) * array(weight_n) / (array(weight_d) + theta))
	return weight_mat, feature_mat
