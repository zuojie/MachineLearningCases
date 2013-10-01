#encoding=utf-8
import datetime
import multiprocessing
import random, traceback
#from getdatV1 import *
import getdatV1

if __name__ == "__main__":
	start_t = datetime.datetime.now()
	page_index = [(30, 40), (40, 50)]
	ps = []
	for i in range(len(page_index)):
    		ps.append(multiprocessing.Process(target=getdatV1.Run, args=(page_index[i][0], page_index[i][1])))
	for process in ps:
		process.start()
	for process in ps:
    		process.join()
    	#p1 = multiprocessing.Process(target=getdatV1.Run, args=(page_index[0][0], page_index[0][1]))
	#p1.start()
	#p1.join()
	end_t = datetime.datetime.now()
	interval = (end_t - start_t).seconds 
	print interval
