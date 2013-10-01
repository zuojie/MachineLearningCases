#encoding=utf-8
import sys

if len(sys.argv) < 1:
	print "no file!"
	sys.exit(0)

fname_in = sys.argv[1]
#fname_out = fname_in + ".format"
fname_out = "dianping_zi_chu_can_item_based.txt"
print fname_in
fin = open(fname_in, "r")
fout = open(fname_out, "ab")

i = 0
while True:
	line = fin.readline()
	i += 1
	if not line:
		break
	if i % 2 == 0: continue
	fout.write(line)

fin.close()
fout.close()
