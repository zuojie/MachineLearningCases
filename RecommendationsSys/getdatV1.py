#encoding=utf-8
import sys, re
import random, traceback
import urllib2
from bs4 import *

domain = "http://www.dianping.com"
city = 2 #北京 
huo_guo = 110 #火锅
zi_zhu_can = 111
xi_can = 116
category = "http://www.dianping.com/search/category/%s/10/g%s" % (city, zi_zhu_can)
comment_per_page = 20
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

def PrintText(txt):
	print txt.encode('gbk', 'ignore')

def ProcessUL(shop_name, ul, res_dict):
	for li in ul("li"):
		spans = li.find_all("span")
		span_index = 1
		star = "-"
		try:
			name = li.p.get_text()
			try:
				star = spans[span_index]["title"]
			except Exception, e: 
				span_index -= 1
				msg = traceback.format_exc()
				print msg
				pass
			span_index += 1
			class_name = spans[span_index]["class"][0]
			cost_per_customer = "-"
			if class_name == 'comm-per':
				cost_per_customer = spans[span_index].get_text()
				span_index += 1
			taste = spans[span_index].get_text()
			span_index += 1
			environment = spans[span_index].get_text()
			span_index += 1
			service = spans[span_index].get_text()
			'''
			PrintText(name)
			PrintText(star)
			PrintText(cost_per_customer)
			PrintText(taste)
			PrintText(environment)
			PrintText(service)
			#print '-----------------'
			'''
			if shop_name not in res_dict.keys():
				res_dict.setdefault(shop_name, [])
			res_dict[shop_name].append([name, star, cost_per_customer, taste, environment, service])
		except Exception, e:
			msg = traceback.format_exc()
			print msg
			continue

def ParsePage(shop, pages, res_dict):
	for page in pages:
		print "parseing %s" % page
		try:
			req = urllib2.Request(url = page,
					headers = headers)
			c = urllib2.urlopen(req, timeout=15)
			soup = BeautifulSoup(c.read(), from_encoding="utf-8")
			divs = soup.find_all(id="revFlt")[0]
			comment_filter = divs.parent.parent
			comment_list = comment_filter.next_sibling.next_sibling
			ul = comment_list("ul")[0]
		except Exception, e:
			msg = traceback.format_exc()
			print msg
			continue
		ProcessUL(shop, ul, res_dict)

def Crawl(shop_url_dict, depth = 1):
	p = re.compile(r"\d+")
	res_dict = {}
	for i in range(depth):
		#newPages = set()
		for (shop, page) in shop_url_dict.items():
			try:
				req = urllib2.Request(url = page,
						headers = headers)
				c = urllib2.urlopen(req)
				soup = BeautifulSoup(c.read(), from_encoding="utf-8")
				divs = soup.find_all(id="J_comment-list-cont")
				comments = divs[0].find_all("a", rel="nofollow")[-1].get_text().encode("gbk", "ignore")
				tot_comment = p.findall(comments)[0]
				tot_comment = int(tot_comment)
				#print tot_comment 
				tot_pages = (tot_comment + comment_per_page - 1) / comment_per_page + 1
				subpages = [page + "/review_all?pageno=" + str(page_idx) for page_idx in range(1, tot_pages)]
				print subpages
				ParsePage(shop, subpages, res_dict)
			except Exception, e:
				msg = traceback.format_exc()
				#print msg
				continue
	return res_dict

def GenerateMemberIds(init_ids, popsize = 50, mutprob_rate = 0.4, step = 1):
	ids = set()
	for id in init_ids:
		ids.add(id)
	lower_bound = 0
	upper_bound = 9
	def mutate(vec, mut_rate = 0.5):
		# 商店id为6位数
		i = random.randint(lower_bound, 5)
		if random.random() < mut_rate and vec[i] > lower_bound:
			return vec[0:i] + ((vec[i] - step),) + vec[i + 1:]
		else:
			return vec[0:i] + ((vec[i] + step) % (upper_bound + 1), ) + vec[i + 1:]
	def crossover(r1, r2):
		i = random.randint(lower_bound, upper_bound)
		return r1[0:i] + r2[i:]
	while len(ids) < popsize:
		ids_list = list(ids)
		idx = int(random.randint(0, len(ids) - 1))
		r1 = ids_list[idx]
		if random.random() < mutprob_rate or len(ids) < 2:
			c = mutate(r1)
			#print "mutate", "".join([str(i) for i in c])
			ids.add(c)
		else:
			idx2 = int(random.randint(0, len(ids) - 1))
			if idx == idx2: idx2 = (idx + step) % len(ids_list) 
			r2 = ids_list[idx2]
			c = crossover(r1, r2)
			#print "crossover", "".join([str(i) for i in c])
			ids.add(c)
	#return list(ids)
	#return [[str(i) for i in j] for j in ids]
	return ["".join([str(i) for i in j]) for j in ids]

# by default, just get page first
def ParseMemberID(url, start_page = 1, end_page = 2):
	shop_url_dict = {}
	url += "p%s"
	for i in range(start_page, end_page):
		try:
			page = url % i
			print "ParseMemberID: " + page
			req = urllib2.Request(url = page,
					headers = headers)
			c = urllib2.urlopen(req)
			soup = BeautifulSoup(c.read(), from_encoding="utf-8")
			search_list = soup.find_all(id="searchList")[0]
			dl = search_list("dl")[0]
			# href = /shop/123456
			href = dl.find_all("a", href=re.compile("shop/\d+$"))
			for ref in href:
				PrintText(ref.get_text())
				shop_name = ref.get_text()
				shop_url = domain + ref["href"]
				print shop_url
				if shop_name not in shop_url_dict.keys():
					shop_url_dict[shop_name] = shop_url 
		except Exception, e:
			msg = traceback.format_exc()
			print msg
			continue
	return shop_url_dict

def PrintResDict(res_dict, file_handler = True, fname = "res_v2.txt"):
	if file_handler == True:
		f = open(fname, "w")
		try:
			for key in res_dict.keys():
				first_1 = True
				f.write(key.encode("utf-8") + ":")
				for val in res_dict[key]:
					first_2 = True
					if first_1 == True:
						first_1 = False
					else:
						f.write(",")
					for v in val:
						if first_2 == True:
							first_2 = False
						else:
							f.write("|")
						f.write(v.encode("utf-8"))
				f.write("\n")
		except:
			f.close()
			return
		f.close()
	else:
		for key in res_dict.keys():
			PrintText(key)
			for val in res_dict[key]:
				for v in val:
					PrintText(v)
				print '-------------------------------'
			print '======================='
#[start_page, end_page)
def Run(start_page, end_page):
	res_dict = {}
	shop_url_dict = {}
	shop_url_dict = ParseMemberID(category, start_page, end_page)
	res_dict = Crawl(shop_url_dict)
	fname = "dianping_zi_chu_can_" + str(start_page) + "_" + str(end_page - 1) + ".txt"
	print fname
	PrintResDict(res_dict, True, fname)

if __name__ == "__main__":
	init_ids = [(5, 1, 3, 7, 6, 2)]
	#memberids = GenerateMemberIds(init_ids, 5)
	#memberids = ParseMemberID(category)
	#抓取到第page_idx页
	page_idx = 1
	shop_url_dict = {}
	ParseMemberID(category, page_idx)
	Crawl(shop_url_dict)
	PrintResDict(res_dict)
