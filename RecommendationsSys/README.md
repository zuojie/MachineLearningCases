Recommendation System
==================

A Recommendation System prototype for www.dianping.com   
* data contains the dianping.com data file   
* getdat_master.py is response to crawling the reviews from dianping.com
* file_process.py preprocesses the raw data, including cleaning up
* file_process_str2id.py is response to transfering item and user to id
* recommendations.py contains a series of recommendations algorithm, the recommned behaviour happened here. Based on Slope One and Collaborative Filtering

____
一个基于大众点评网的点评数据编写的推荐系统原型，可以为指定用户推荐火锅店或者为指定火锅店推荐潜在客户   
* data目录包含从大众点评网获取的用户评论数据
* getdat_master.py负责数据d抓取，采用多进程同步抓取的方式
* file_process.py负责对原始数据的预处理和清洗
* file_process_str2id.py负责把商户名称和用户名称转换为id表示的形式
* recommendations.py是进行实际推荐的文件，推荐算法基于Slope One和协同过滤
