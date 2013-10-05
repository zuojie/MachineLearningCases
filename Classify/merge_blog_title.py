#encoding=utf-8
# author: zuojie peng

def run():
	fo = open("data/blog_title.txt", "w")
	f = "data/title/%s"
	for i in range(5000):
		fi = open(f % i, "r")
		fo.write(fi.readline() + "\n")
	fo.close()

if __name__ == "__main__":
	run()

