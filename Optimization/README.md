##### Implements a system like StumbleUpon by means of Simulated Annealing and Genetic Algorithm. We use them to optimize our brute force solution
Problem comes as follows:
* User A has a like keywords list, in which the keywords have different weighting. like -> dislike => high weighting -> low weighting
* We have a web sites list, in which all the web sites are labeld by some keywords, for example *technology, food, movie etc* 
* We should recommend X web sites for user A in purpose of satifying user A as much as possible

___

##### 通过模拟退火算法和遗传算法来实现一个类似StumbleUpon的网址推荐系统，模拟退火和遗传算法这里主要是为了优化暴力搜索解空间引入的性能问题
问题描述如下：   
* 用户A有一系列喜好关键词列表，不同关键词权重不同，和喜好程度成正比  
* 我们有一个网站列表，这些网站被不同的关键词所标注
* 我们要为用户A推荐X个网址，需要使用户A的满意度尽可能的大
