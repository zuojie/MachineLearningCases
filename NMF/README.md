###Finding independent features can help us find the common features exist in the data and help us make a predict about it
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
比赛提供一些没有标记的训练数据，需要我们先基于规则的方法来进行预处理标记，这个方法来自[康师傅](http://www.bottomcoder.ru/wordpress/archives/78#comment-136).抛开细节不说，正规军都是用博客的摘要和正文来进行训练的，我直接偷懒使用了博客标题来进行训练
和最终的测试，结果见相关文件，马马虎虎差强人意吧。目前成绩最好的是康师傅的88%左右的误差记录。各文件功能性说明见上，不再赘述。

___

###详见:  
[被嗶哩嗶哩抛弃的人](http://zuojie.github.io/2013/11/30/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E5%AE%9E%E8%B7%B5%3A%E8%A2%AB%E5%97%B6%E5%93%A9%E5%97%B6%E5%93%A9%E6%8A%9B%E5%BC%83%E7%9A%84%E4%BA%BA.html)

