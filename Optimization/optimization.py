#encoding=utf8
import random, math 

# p = e^(-(hightcost - lowcost) / temperature)
def AnnealingOptimize(domain, costf, T = 10000.0, cool_rate = 0.95, step = 1):
	vec = [float(random.randint(domain[i][0], domain[i][1])) for i in rang(len(domain))]
	while T > 0.1:
		i = random.randint(0, len(domain) - 1)
		dir = random.randint(-step, step)
		new_vec = vec[:]
		new_vec[i] += dir
		if new_vec[i] < domain[i][0]: new_vec[i] = domain[i][0]
		if new_vec[i] > domain[i][1]: new_vec[i] = domain[i][1]
		cost = costf(vec)
		new_cost = costf(new_vec)
		if (cost > new_cost or random.random() < pow(math.e, -(new_cost - cost) / Ta)):
			vec = new_vec
		T = T * cool_rate
	return vec

