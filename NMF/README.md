###Finding independent features can help us find the common features exist in the data and help us make predicts about it
This case is cluster-like algorithm(Non-Negative Matrix Factorization) to find the common features within users and their comments of www.bilibili.tv   
* nmf.py is the NMF algorithm lib
* feature_extract.py is the main script, response for preprocessing data, make origin data matrix etc
* get_bilibili_dat.py is parser to parse bilibili blacklist users table
* ./data/badlist.table is the source code file 
* ./data/blacklist.txt is the users and comments  
* ./data/cut.txt is the comments words processed by jieba splitter 
* ./data/features.txt and ./data/user_feature.txt is the result data
* ./jieba/ and ./extra_dict/ is a [Python Chinese segmentation module](https://github.com/fxsjy/jieba) used in my code
* ./extra_dict/ is user defined dictionary used by jieba

___

###通过对数据矩阵进行因子分解，我们可以发现数据中潜在的独立特征.
详见:  
[被嗶哩嗶哩抛弃的人](http://zuojie.github.io/2013/11/30/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E5%AE%9E%E8%B7%B5%3A%E8%A2%AB%E5%97%B6%E5%93%A9%E5%97%B6%E5%93%A9%E6%8A%9B%E5%BC%83%E7%9A%84%E4%BA%BA.html)

