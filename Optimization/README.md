##### Implements a system like StumbleUpon by means of Simulated Annealing and Genetic Algorithm. We use them to optimize our brute force solution
Problem comes as follows:
* User A has a like keywords list, in which the keywords have different weighting. like -> dislike => high weighting -> low weighting
* We have a web sites list, in which all the web sites are labeld by some keywords, for example *technology, food, movie etc* 
* We should recommend X web sites for user A in purpose of satifying user A as much as possible
optimization.py is the optimization algorithm lib, the problem must fit the needs as follow if it wanted to be sloved by the lib:   
* Solution can be described as integer list
* The solution can be converted as a number, which implies it's cost. Optimizaion algorithm will choose the best answer that costs least
___

##### 通过模拟退火算法和遗传算法来实现一个类似StumbleUpon的网址推荐系统，模拟退火和遗传算法这里主要是为了优化暴力搜索解空间引入的性能问题
问题描述如下：   
* 用户A有一系列喜好关键词列表，不同关键词权重不同，和喜好程度成正比  
* 我们有一个网站列表，这些网站被不同的关键词所标注
* 我们要为用户A推荐X个网址，需要使用户A的满意度尽可能的大
optimization.py是优化算法库，里面实现了模拟退火和遗传算法（可灵活扩展增加优化函数）.如果想使用这个库解决问题，这个问题必须符合如下形式:   
* 解空间能用数字列表表示
* 解空间能被转化成一个成本值（通过一个成本函数，计算给定解空间需要耗费的成本）,以方便优化算法来对解空间进行合理取舍
