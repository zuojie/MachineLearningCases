#encoding=utf-8
# author: zuojiepeng
from PIL import Image, ImageDraw, ImageFont

class bicluster:
	def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
		self.left = left
		self.right = right 
		self.vec = vec 
		self.id = id 
		self.distance = distance 

def Hcluster(rows, dis_func):
	distances = {}
	current_id = -1
	clusts = [bicluster(rows[i], id=i) for i in range(len(rows))]
	while len(clusts) > 1:
		lowest_pair = (0, 1)
		closest = dis_func(clusts[lowest_pair[0]].vec, clusts[lowest_pair[1]].vec)
		for i in range(len(clusts)):
			for j in range(i + 1, len(clusts)):
				if (clusts[i].id, clusts[j].id) not in distances:
					distances[(clusts[i].id, clusts[j].id)] = dis_func(clusts[i].vec, clusts[j].vec)
				d = distances[(clusts[i].id, clusts[j].id)]
				if d < closest:
					closest = d
					lowest_pair = (i, j)
		merge_vec = [(clusts[lowest_pair[0]].vec[i] + clusts[lowest_pair[1]].vec[i]) / 2.0 
					for i in range(len(clusts[0].vec))] 
		new_clust = bicluster(merge_vec, left = clusts[lowest_pair[0]], 
							right = clusts[lowest_pair[1]],
							distance = closest, id = current_id)
		current_id -= 1
		del clusts[lowest_pair[1]]
		del clusts[lowest_pair[0]]
		clusts.append(new_clust)
	return clusts[0]

def PrintClust(clust, labels = None, n = 0):
	for i in range(n): print ' ',
	if clust.id < 0: print '-'
	else:
		if labels == None: print clust.id
		else: print labels[clust.id]
	if clust.left != None: PrintClust(clust.left, labels = labels, n = n + 1)
	if clust.right != None: PrintClust(clust.right, labels = labels, n = n + 1)

def GetHeight(clust):
	if clust.left == None and clust.right == None: return 1
	return GetHeight(clust.left) + GetHeight(clust.right)

def GetDepth(clust):
	if clust.left == None and clust.right == None: return 0
	return max(GetDepth(clust.left), GetDepth(clust.right)) + clust.distance

def DrawDendrogram(clust, labels, jpeg = "clusters.jpg"):
	h = GetHeight(clust) * 20
	w = 1200
	depth = GetDepth(clust)
	scaling = float(w - 150) / depth
	img = Image.new("RGB", (w, h), (255,) * 3)
	draw = ImageDraw.Draw(img)
	draw.line((0, h / 2, 10, h / 2), fill = (255, 0, 0))
	DrawNode(draw, clust, 10, h / 2, scaling, labels)
	img.save(jpeg, "JPEG")

font_path = "Fonts/msyh.ttc"
my_font = ImageFont.truetype(font_path, 24)
def DrawNode(draw, clust, x, y, scaling, labels):
	if clust.id < 0:
		hl = GetHeight(clust.left) * 20
		hr = GetHeight(clust.right) * 20
		top = y - (hl + hr) / 2
		bottom = y + (hl + hr) / 2
		ll = clust.distance * scaling
		draw.line((x, top + hl / 2, x, bottom - hr / 2), fill = (255, 0, 0))
		draw.line((x, top + hl / 2, x + ll, top + hl / 2), fill = (255, 0, 0))
		draw.line((x, bottom - hr / 2, x + ll, bottom - hr / 2), fill = (255, 0, 0))
		DrawNode(draw, clust.left, x + ll, top + hl / 2, scaling, labels)
		DrawNode(draw, clust.right, x + ll, bottom - hr / 2, scaling, labels)
	else: draw.text((x + 5, y - 7), unicode(labels[clust.id].decode("utf8").encode("utf8"), "utf8"), fill = (0,) * 3, font = my_font)
