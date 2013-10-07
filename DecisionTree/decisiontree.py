#encoding=utf-8
# author: zuojie peng
from math import log
from PIL import Image, ImageDraw, ImageFont
 
font_path = "Fonts/msyh.ttc"
my_font = ImageFont.truetype(font_path, 20)
my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode:
	def __init__(self, col = -1, value = None, results = None, tb = None, fb = None):
		self.col = col
		self.value = value
		self.results = results
		self.tb = tb
		self.fb = fb

def DivideSet(rows, col, value):
	split_func = None
	if isinstance(value, int) or isinstance(value, float):
		split_func = lambda row:row[col] >= value
	else:
		split_func = lambda row:row[col] == value
	list_true = [row for row in rows if split_func(row)]
	list_false = [row for row in rows if not split_func(row)]
	return (list_true, list_false)

def UniqueCnt(rows):
	res = {}
	for row in rows:
		r = row[len(row) - 1]
		if r not in res: res[r] = 0
		res[r] += 1
	return res

def GiniImpurity(rows):
	total = len(rows)
	cnts = UniqueCnt(rows)
	imp = 0
	for k1 in cnts:
		p = float(cnts[k1]) / total
		imp += p * (1 - p)
	return imp

#ID3
def Entropy(rows):
	log2 = lambda x:log(x)/log(2)
	res = UniqueCnt(rows)
	ent = 0.0
	for r in res.keys():
		p = float(res[r]) / len(rows)
		ent = ent - p * log2(p)
	return ent

#numerical
def Variance(rows):
	if len(rows) == 0: return 0
	else: 
		data = []
		data = [float(row[-1]) for row in rows]  
		mean = sum(data) / len(rows)
		variance = sum([(d - mean) ** 2 for d in data]) / len(data)
		return variance

def BuildTree(rows, ScoreF = Entropy):
	if len(rows) == 0: return decisionnode()
	current_score = ScoreF(rows)
	best_gain = 0.0
	best_criteria = None
	best_sets = None
	column_cnt = len(rows[0]) - 1
	for col in range(0, column_cnt):
		for row in rows:
			list_true, list_false = DivideSet(rows, col, row[col])
			weight = float(len(list_true)) / len(rows)
			info_gain = current_score - weight * ScoreF(list_true) - (1 - weight) * ScoreF(list_false)
			if info_gain > best_gain and len(list_true) > 0 and len(list_false) > 0:
				best_gain = info_gain
				best_criteria = (col, row[col])
				best_sets = (list_true, list_false)
	if best_gain > 0:
		true_branch = BuildTree(best_sets[0], ScoreF)
		false_branch = BuildTree(best_sets[1], ScoreF)
		return decisionnode(col = best_criteria[0], value = best_criteria[1], tb = true_branch, fb = false_branch)
	return decisionnode(results = UniqueCnt(rows))

def Prune(tree, gain_low_boundry):
	if tree == None: return
	if tree.tb.results == None:
		Prune(tree.tb, gain_low_boundry)
	if tree.fb.results == None:
		Prune(tree.fb, gain_low_boundry)
	if tree.fb.results != None and tree.tb.results != None:
		tb, fb = [], []
		for v, c in tree.tb.results.iteritems():
			tb += [[v]] * c
		for v, c in tree.fb.results.iteritems():
			fb += [[v]] * c
		weight = len(tb) / (len(tb) + len(fb)) 
		delta = Entropy(tb + fb) - (weight * Entropy(tb) + (1 - weight) * Entropy(fb))
		if delta < gain_low_boundry:
			tree.tb, tree.fb = None, None
			tree.results = UniqueCnt(tb + fb)

def PrintTree(node, indent = 0):
	if node.results != None: print str(node.results)
	else:
		print str(node.col) + ":" + str(node.value) + "? "
		print " " * indent + "T->",
		PrintTree(node.tb, indent + 1)
		print " " * indent + "F->",
		PrintTree(node.fb, indent + 1)

def Classify(row, tree):
	if tree.results != None: return tree.results
	else:
		v = row[tree.col]
		branch = None
		if isinstance(v, int) or isinstance(v, float):
			if v >= tree.value: branch = tree.tb
			else: branch = tree.fb
		else:
			if v == tree.value: branch = tree.tb
			else: branch = tree.fb
		return Classify(row, branch)

def LostFixClassify(row, tree):
	if tree == None: return []
	if tree.results != None: return tree.results
	else:
		v = row[tree.col]
		# lost
		if v == None:
			tr, fr = LostFixClassify(row, tree.tb), LostFixClassify(row, tree.fb)
			tcnt = sum(tr.values())
			fcnt = sum(fr.values())
			tw = float(tcnt) / float(tcnt + fcnt)
			fw = 1 - tw
			res = {}
			for k, v in tr.items(): res[k] = v * tw
			for k, v in fr.items(): 
				if k not in res: res[k] = 0
				res[k] += v * fw
			return res
		else:
			if isinstance(v, int) or isinstance(v, float):
				if v >= tree.value: branch = tree.tb
				else: branch = tree.fb
			else:
				if v == tree.value: branch = tree.tb
				else: branch = tree.fb
			return LostFixClassify(row, branch)

def GetWidth(tree):
	if tree == None: return 0
	if tree.tb == None and tree.fb == None: return 1
	return GetWidth(tree.tb) + GetWidth(tree.fb)

def GetDepth(tree):
	if tree == None: return 0
	if tree.tb == None and tree.fb == None: return 1
	return max(GetDepth(tree.tb), GetDepth(tree.fb)) + 1

def DrawNode(draw, tree, x, y):
	if tree.results == None:
		fw = GetDepth(tree.fb) * 100
		tw = GetDepth(tree.tb) * 100
		left = x -  tw / 2
		right = x + fw / 2
		if tree.col == 2: val = str(tree.value)
		else: val = unicode(tree.value.decode("utf8").encode("utf8"), "utf8")
		draw.text((x - 20, y - 10), str(tree.col) + ":" + val, (0,) * 3, font = my_font)
		draw.line((x, y, left, y + 100), fill = (255, 0, 0))
		draw.text((x - (x - left) / 2 - 15, y + 100 / 2), "F", (0, 255, 0), font = my_font)
		draw.line((x, y, right, y + 100), fill = (255, 0, 0))
		draw.text((x + (right  - x) / 2, y + 100 / 2), "T", (0, 255, 0), font = my_font)
		DrawNode(draw, tree.fb, left, y + 100)
		DrawNode(draw, tree.tb, right, y + 100)
	else:
		y_axis = y
		for v in tree.results.items():
			txt = "%s:%d" % v
			draw.text((x - 20, y_axis), txt, (0,) * 3) 
			y_axis += 13

def DrawTree(tree, jpeg = "tree.jpg"):
	w = GetWidth(tree) * 80 + 120
	h = GetDepth(tree) * 100 + 220
	img = Image.new("RGB", (w,h), (255,) * 3)
	draw = ImageDraw.Draw(img)
	# 从画布宽度的中间，距离顶部20px处开始作画
	DrawNode(draw, tree, w / 2, 20)
	img.save(jpeg, "JPEG")

def Run():
	#print DivideSet(my_data, 2, "yes")
	print GiniImpurity(my_data)
	print Entropy(my_data)
	list1, list2 = DivideSet(my_data, 2, "yes")
	print GiniImpurity(list1)
	print Entropy(list1)
	dt = BuildTree(my_data)
	#PrintTree(dt)
	#DrawTree(dt, "desicion_tree.jpg")
	Prune(dt, 1.0)
	DrawTree(dt, "desicion_tree_prune.jpg")
	#print Classify(["(direct)", "USA", "yes", 5], dt)
	print LostFixClassify(["google", None, "yes", None], dt)
	print LostFixClassify(["google", "France", None, None], dt)

if __name__ == "__main__":
	Run()
	

