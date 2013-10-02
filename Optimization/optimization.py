#encoding=utf8
import random, math 

# p = e^(-(hightcost - lowcost) / temperature)
def AnnealingOptimize(domain, costf, T = 10000.0, cool_rate = 0.95, step = 1):
	vec = [float(random.randint(domain[i][0], domain[i][1])) for i in range(len(domain))]
	while T > 0.1:
		i = random.randint(0, len(domain) - 1)
		dir = random.randint(-step, step)
		new_vec = vec[:]
		new_vec[i] += dir
		if new_vec[i] < domain[i][0]: new_vec[i] = domain[i][0]
		if new_vec[i] > domain[i][1]: new_vec[i] = domain[i][1]
		cost, real_v = costf(vec)
		new_cost, real_newv = costf(new_vec)
		if (cost > new_cost or random.random() < pow(math.e, -(new_cost - cost) / T)):
			vec = new_vec
			real_v = real_newv
			print new_cost, real_v
		T = T * cool_rate
	return real_v 

def GeneticOptimize(domain, costf, pop_size = 50, step = 1,
					mut_prob = 0.2, elite = 0.2, max_iter = 100):
	def mutate(vec):
		i = random.randint(0, len(domain) - 1)
		v = vec[i]
		if random.random() < 0.5:
			if vec[i] - step >= domain[i][0]: v = vec[i] - step
			elif vec[i] + step <= domain[i][1]: v = vec[i] + step
		else:
			if vec[i] + step <= domain[i][0]: v = vec[i] + step
			elif vec[i] - step >= domain[i][1]: v = vec[i] - step
		return vec[0:i] + [v] + vec[i + 1:]
	def crossover(v1, v2):
		i = random.randint(1, len(domain) - 2)
		return v1[0:i] + v2[i:]
	init_pop = []
	for i in range(pop_size):
		vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
		init_pop.append(vec)
	top_elite = int(elite * pop_size)
	for i in range(max_iter):
		scores = [(costf(v), v) for v in init_pop]
		scores.sort()
		ranked = [v for (score, v) in scores]
		real_ranked = [score[1] for (score, v) in scores]
		init_pop = ranked[0:top_elite]
		while len(init_pop) < pop_size:
			v_i = random.randint(0, top_elite)
			if random.random() < mut_prob:
				init_pop.append(mutate(ranked[v_i]))
			else:
				v_i2 = random.randint(0, top_elite)
				init_pop.append(crossover(ranked[v_i], ranked[v_i2]))
		print scores[0][0], scores[0][1]
	return real_ranked[0]

if __name__ == "__main__":
	pass
