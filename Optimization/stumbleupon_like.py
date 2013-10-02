#encoding=utf8
from optimization import *

user = {"food":-5, "reading":-4, "painting":-3, "music":-2, "game":-1}
X = 6
sites = {0:"zuojie.github.io",
		1:"a.com",
		2:"b.com",
		3:"c.com",
		4:"d.com",
		5:"e.com",
		6:"f.com",
		7:"g.com",
		8:"h.com",
		9:"i.com",
		10:"j.com",
		11:"k.com",
		12:"l.com",
		}

web_sites = {"zuojie.github.io":("news", "food", "programming"),
			"a.com":("food", "game"),
			"b.com":("food", "painting", "music"),
			"c.com":("reading", "painting"),
			"d.com":("video", "reading", "music"),
			"e.com":("music",),
			"f.com":("food",),
			"g.com":("food", "reading", "art"),
			"h.com":("music", "football", "art"),
			"i.com":("tv", "basketball", "car"),
			"j.com":("painting", "music", "car"),
			"k.com":("painting", "music", "car"),
			"l.com":("painting", "music")
			}
# 一个很碉堡的条件设定, 有效防止非法解的出现
domain = [(0, len(web_sites) - i - 1) for i in range(X)]
# not cool
#domain = [(0, len(web_sites)] * X

def PrintSolution(vec):
	slots = [i for i in range(len(sites))]
	for i in range(len(vec)):
		idx = int(vec[i])
		j = slots[idx]
		site = sites[j]
		print site
		# not cool
		#del slots[idx]


def Costf(vec):
	slots = [i for i in range(len(sites))]
	cost = 0
	new_v = []
	for i in range(len(vec)):
		idx = int(vec[i])
		j = slots[idx]
		new_v += [j]
		site = sites[j]
		keywords = web_sites[site]
		minus = False
		for key in keywords: 
			if key not in user:
				if False == minus: 
					cost += 1
					minus = True
			else: 
				cost += user[key]
		del slots[idx]
	'''
	print "before ", vec 
	print "after ", new_v
	'''
	return cost, new_v 

# check the pitfall of python list pass by reference
def test2(v):
	newv = [8,8]
	v = newv
	#v = -v[0]
	return v

def test():
	v = [[-1,1], [8, 9]]
	print v
	v2 = [(test2(vv), vv) for vv in v]
	print v2

if __name__ == "__main__":
	#vec = GeneticOptimize(domain, Costf, pop_size = 13, max_iter = 25)
	vec = AnnealingOptimize(domain, Costf)
	PrintSolution(vec)
