#encoding=utf-8
import sys, re
from math import sqrt

fname_in = "data/dianping_huoguo_item_based.txt"
fname_addr_out = "data/dianping_huoguo_user_addr_based.txt"
fname_out = "data/dianping_huoguo_user_based.txt"
fname_out_dr = "data/dianping_huoguo_user_based_dr.txt"
fname_out_sample = "data/dianping_huoguo_user_based_sample.txt"

star_dict = {}
env_dict = {}
user_based_dict = {}

def DecodeAsUTF8(val):
	return val.decode("utf-8", "ignore")

def DecodeAsGBK(val):
	return val.decode("gbk", "ignore")

# change terminal_encode if needed
def Str2Unicode(val, terminal_encode = "gbk"):
	return unicode(val, terminal_encode)

def SimExEuclid(person1, person2, prefs = user_based_dict):
	si = []
	# 只去过一家店的食客不考虑
	if len(prefs[person2]) < 2: return 0
	for item in prefs[person1]:
		if item in prefs[person2]: si.append(item)
	if len(si) == 0: return 0
	sum_of_squares = 0
	for item in si:
		# 如果二者对于某家店的评价相似，并且都是不喜欢, 则将二者差距翻1.5倍并加固定值,注意都为0的情况
		d_val = pow(prefs[person1][item] - prefs[person2][item], 2)
		#d_val = abs(prefs[person1][item] - prefs[person2][item])
		sum_of_squares += d_val
	#sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]])
	return len(si) / (len(si) + sqrt(sum_of_squares))
	#return 1.0 / (1.0 + sqrt(sum_of_squares))

def SimPearson(person1, person2, prefs = user_based_dict):
	si = []
	if len(prefs[person2]) < 2: return 0
	for item in prefs[person1]:
		if item in prefs[person2]: si.append(item)
	n = len(si)
	if n == 0: return 1
	sum1 = sum([prefs[person1][i] for i in si])
	sum2 = sum([prefs[person2][i] for i in si])
	sqrt1 = sum([pow(prefs[person1][i], 2) for i in si])
	sqrt2 = sum([pow(prefs[person2][i], 2) for i in si])
	p_sum = sum([prefs[person1][i] * prefs[person2][i] for i in si])
	num = p_sum - (sum1 * sum2 / n)
	den = sqrt((sqrt1 - pow(sum1, 2) / n) * (sqrt2 - pow(sum2, 2) / n))
	if den == 0: return 0
	r = num / den
	return r

def TopMatches(person, n = 25, prefs = user_based_dict, sim_func = SimExEuclid):
	scores = [(sim_func(person, oth, prefs), oth) for oth in prefs if oth != person]
	scores.sort()
	scores.reverse()
	return scores[0:n]

def GetRecommendations(person, n = 10, prefs = user_based_dict, sim_func = SimExEuclid):
	totals = {}
	sim_sums = {}
	kw = "我只是飘过"
	kw2 = unicode(kw, "gbk")
	for oth in prefs:
		if oth == person: continue
		sim = sim_func(person, oth, prefs)
		#if oth == "aprilxw" or DecodeAsUTF8(oth) == kw2: print DecodeAsUTF8(oth), sim
		if sim <= 0: continue
		for item in prefs[oth]:
			# person没有吃过这家店
			if item not in prefs[person]:
				totals.setdefault(item, 0)
				# 品味相似者对这家店的评价 * 和相似者的相似度
				totals[item] += prefs[oth][item] * sim
				sim_sums.setdefault(item, 0)
				#sim_sums[item] += sim
				### 避免10 * (0.1 + 0.1 + 0.1) / (0.1 + 0.1 + 0.1)的情况,改为除以评价人数
				sim_sums[item] += 1 

	rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
	rankings.sort()
	rankings.reverse()
	return rankings[0:n]

def GetRecommendedItemds(item_match, person, prefs, n = 50):
	user_ratings = prefs[person]
	scores = {}
	total_sim = {}
	for (item, rating) in user_ratings.items():
		for (sim, item2) in item_match[item]:
			if item2 in user_ratings: continue
			scores.setdefault(item2, 0)
			scores[item2] += sim * rating
			total_sim.setdefault(item2, 0)
			# 考虑相似度为权值，类似slope one
			total_sim[item2] += sim
	rankings = [(score / total_sim[item], item) for (item, score) in scores.items()]
	rankings.sort()
	rankings.reverse()
	#return rankings[0:n]
	return rankings

def FixShop(val):
	tp = val.split("(")
	return tp[0]

def PreProcess(fin, fout, keep_addr = False):
	st = Str2Unicode("很好")
	star_dict[st] = 2
	st = Str2Unicode("好")
	star_dict[st] = 1
	st = Str2Unicode("还行")
	star_dict[st] = 0
	st = Str2Unicode("差")
	star_dict[st] = -1
	st = Str2Unicode("很差")
	star_dict[st] = -2
	st = Str2Unicode("非常好")
	env_dict[st] = 3
	st = Str2Unicode("很好")
	env_dict[st] = 2
	st = Str2Unicode("好")
	env_dict[st] = 1
	st = Str2Unicode("一般")
	env_dict[st] = 0
	st = Str2Unicode("差")
	env_dict[st] = -1 

	fi = open(fin, "r")
	fo = open(fout, "w")
	p = re.compile(r"\d+")
	while True:
		line = fi.readline()
		if not line: break
		info = line.split(":")
		shop = info[0]
		if keep_addr == False: shop = FixShop(shop)
		#print DecodeAsUTF8(shop)
		#continue
		users = info[1].split(",")
		for user in users:
			try:
				comment = user.split("|")
				uname = DecodeAsUTF8(comment[0])
				'''
				try:
					print uname
				except Exception, e:
					continue
				'''
				star = DecodeAsUTF8(comment[1])
				if star == '-': star = 0
				else: star = star_dict[star]
				taste = int(p.findall(comment[3])[0])
				taste -= 1
				env = int(p.findall(comment[4])[0])
				env -= 1
				service = int(p.findall(comment[5])[0])
				service -= 1
				score = taste * 1.5 + env + service
				val = shop + ":" + str(score)
				#print DecodeAsUTF8(val)
				if uname not in user_based_dict.keys(): user_based_dict.setdefault(uname, [])
				user_based_dict[uname].append(val)
				#print uname, star, taste, env, service
			except IndexError, ie:
				continue
			except KeyError, ie:
				print uname
				continue
	#print user_based_dict
	for user_name, shop in user_based_dict.items():
		fo.write(user_name.encode("utf-8") + "|")
		first = True 
		dic_tp = {}
		dic_cnt = {}
		# 把同一个店的不同分店信息进行分组聚合求均值
		for sp in shop:
			name, score = sp.split(":")
			dic_tp.setdefault(name, 0.0)
			dic_cnt.setdefault(name, 0)
			dic_tp[name] += float(score) 
			dic_cnt[name] += 1 
		for name, score in dic_tp.iteritems():
			dic_tp[name] /= dic_cnt[name]
		#dic_tp = dict([(name, dic_tp[name] / dic_cnt[name]) for name in dic_tp.iteritems()])
		for sp, score in dic_tp.iteritems():
			if first == True: first = False
			else: fo.write(",")
			fo.write(str(sp) + ":" + str(score))
		fo.write("\n")
	fi.close()
	fo.close()

def DimensionalityReduction(fout, threshold = 0.0001, prefs = user_based_dict):
	rating_sums = {}
	for user in prefs:
		for item in prefs[user]:
			rating_sums.setdefault(item, 0)
			rating_sums[item] += 1 
	fo = open(fout, "w")
	user_len = len(prefs)
	low_bound = threshold * user_len
	for user_name, shop in user_based_dict.iteritems():
		ignore = 0
		for name, score in shop.iteritems():
			if rating_sums[name] <= low_bound:
				ignore += 1
		if ignore == len(shop): continue
		fo.write(user_name + "|")
		first = True 
		for name, score in shop.iteritems():
			# 去除评价次数过低的商户(占比低于0.01%)
			if rating_sums[name] <= low_bound: continue
			if first == True: first = False
			else: fo.write(",")
			fo.write(str(name) + ":" + str(score))
		fo.write("\n")
	fo.close()


def ReadFile2Dict(fname):
	res = {}
	for line in file(fname):
		info = line.split("|")
		user = info[0]
		res.setdefault(user, {})
		#shop = [(shop_name, score) for shop_name, score in ]
		shop = info[1].split(",")
		tp_dict = {}
		tp_cnt = {}
		for i in shop:
			shop_score = i.split(":")
			tp_dict.setdefault(shop_score[0], 0)
			tp_dict[shop_score[0]] += float(shop_score[1])
			tp_cnt.setdefault(shop_score[0], 0)
			tp_cnt[shop_score[0]] += 1
		tp = {}
		for item, score in tp_dict.items():
			tp[item] = score / tp_cnt[item] 
		res[user] = tp
	return res

def TransformPrefs(prefs):
	result = {}
	for person in prefs:
		for item in prefs[person]:
			result.setdefault(item, {})
			result[item][person] = prefs[person][item]
	return result

def CalcSimilarItems(prefs, n = 10):
	res = {}
	item_prefs = TransformPrefs(prefs)
	c = 0
	for item in item_prefs:
		c += 1
		if c % 100 == 0: print "%d / %d" % (c, len(item_prefs))
		#scores = TopMatches(item, n = n, prefs = item_prefs, sim_func = SimPearson)
		scores = TopMatches(item, n = n, prefs = item_prefs)
		res[item] = scores
	return res


diffs = {}
freqs = {}
def InitSlopeOneData(prefs):
	for user, score in prefs.iteritems():
		for item, rating in score.iteritems(): 
			diffs.setdefault(item, {})
			freqs.setdefault(item, {})
			for item2, rating2 in score.iteritems(): 
				diffs[item].setdefault(item2, 0.0)
				freqs[item].setdefault(item2, 0)
				diffs[item][item2] += rating - rating2
				freqs[item][item2] += 1
	for item, ratings in diffs.iteritems():
		for item2, rating in ratings.iteritems(): 
			ratings[item2] /= freqs[item][item2]

def GetRecommendedSlopeOne(person, n, prefs):
	InitSlopeOneData(prefs)
	preds, freq = {}, {}
	try:
		user_profile = prefs[person]
	except KeyError:
		print 'No such user exists'
		return 
	for item, score in user_profile.iteritems():
		for diff_item, diff_rating in diffs.iteritems():
			if item not in freqs[diff_item]: continue
			if diff_item in user_profile: continue
			freq_t = freqs[diff_item][item]
			# 参考mathout实现，不考虑只被一个用户评论的item
			if freq_t == 1: continue
			preds.setdefault(diff_item, 0.0)
			freq.setdefault(diff_item, 0)
			preds[diff_item] += freq_t * (diff_rating[item] + score)
			freq[diff_item] += freq_t
	res = [(score / freq[item], item) for item, score in preds.iteritems() if freq[item] > 0]
	res.sort()
	res.reverse()
	return res[0:n]

def GetTopShop(knn = 15, threshold = 300, popular = True, prefs = user_based_dict):
	res = {}
	for user, ratings in prefs.iteritems(): 
		trick = True 
		for shop, score in ratings.iteritems():
			# 如果评分中有低于满分的, 假设他是个好人
			if score < 16.0: 
				trick = False
				break
		# 如果总共评分不足4家，假设他是个好人
		if trick and len(ratings) < 4: trick = False 
		# 如果这是个坏人，忽略他的评分
		if trick: continue
		for shop, score in ratings.iteritems():
			res.setdefault(shop, [])
			res[shop].append(score)
	ranking = []
	for shop, ratings in res.iteritems(): 
		rating_cnt = {}
		max_r = -1
		min_r = 20
		cnt = len(ratings)
		scores = 0.0
		for rating in ratings:
			if max_r < rating: max_r = rating
			if min_r > rating: min_r = rating
			scores += rating 
			rating_cnt.setdefault(rating, 0)
			rating_cnt[rating] += 1
		# 去除长尾影响，移除出现次数低于5%的最高/低评分
		if rating_cnt[max_r] <= threshold / 60: 
			scores -= max_r * rating_cnt[max_r]  
			cnt -= rating_cnt[max_r]
		if rating_cnt[min_r] <= threshold / 60: 
			scores -= min_r * rating_cnt[min_r]  
			cnt -= rating_cnt[min_r]
		ranking.append((scores / cnt, shop))
	#ranking = [(score / res_cnt[shop], shop) for shop, score in res.iteritems() if res_cnt[shop] >= threshold]
	ranking.sort()
	if popular == True: ranking.reverse()
	return ranking[0:knn]

if __name__ == "__main__":
	#if len(sys.argv) < 1:
		#print "no file!"
		#fname_in = sys.argv[1]
	#PreProcess(fname_in, fname_out)
	#PreProcess(fname_in, fname_addr_out, True)
	#sys.exit(0)

	#user_based_dict = ReadFile2Dict(fname_out)
	#DimensionalityReduction(fout = fname_out_dr, prefs = user_based_dict)
	#sys.exit(0)
	user_based_dict = ReadFile2Dict(fname_out_dr)
	item_based_dict = TransformPrefs(user_based_dict)

	person1 = "banxe"
	person2 = "meiqiu"
	person3 = "red_bogeyman"
	#print SimExEuclid(person1, person2, user_based_dict)
	#person = DecodeAsGBK("劳尔婷").encode("utf-8", "ignore")
	#item = DecodeAsGBK("呷哺呷哺").encode("utf-8", "ignore")
	#item = DecodeAsGBK("香辣阿田大虾火锅").encode("utf-8", "ignore")

	#res = TopMatches(person3, n = 100, prefs = user_based_dict)
	#for score, p in res: print score, DecodeAsUTF8(p).encode("gbk", "ignore")
	#sys.exit(0)
	#res = TopMatches(item, n = 100, prefs = item_based_dict)
	#for score, p in res: print score, DecodeAsUTF8(p).encode("gbk", "ignore")
	item_sim = CalcSimilarItems(user_based_dict)
	knn = 20
	print '[Item CF] 为用户' + DecodeAsUTF8(person3).encode("gbk", "ignore")
	res = GetRecommendedItemds(item_sim, person3, user_based_dict, n = knn)
	for score, p in res: print score, DecodeAsUTF8(p).encode("gbk", "ignore")

	print '----------------------------'

	print '[User CF] 为用户' + DecodeAsUTF8(person3).encode("gbk", "ignore")
	res = GetRecommendations(person3, n = knn, prefs = user_based_dict)
	for score, p in res: print score, DecodeAsUTF8(p).encode("gbk", "ignore")

	print '----------------------------'
	
	print '[Slope One] 为用户' + DecodeAsUTF8(person3).encode("gbk", "ignore")
	res = GetRecommendedSlopeOne(person3, n = knn, prefs = user_based_dict)
	for score, p in res: print score, DecodeAsUTF8(p).encode("gbk", "ignore")
