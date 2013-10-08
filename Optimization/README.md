#####Implements a system like StumbleUpon by means of Simulated Annealing and Genetic Algorithm. We use them to optimize our brute force solution when we solve a NP hard problem   
Problem comes as follows:
* User A has a like keywords list, in which the keywords have different weighting. The weighting is inversely proportional to how much the user liked it
* We have a web sites list, in which all the web sites are labeld by some keywords, for example *technology, food, movie etc* 
* We should recommend X web sites for user A in purpose of satifying user A as much as possible   

>optimization.py is the optimization algorithm lib, the problem must be fitting the needs as follow if it wanted to be sloved by the lib:   

* Solution can be described as integer list
* The solution can be converted as a number, which implies it's cost. Optimizaion algorithm will choose the best answer that costs least
* Cost function must return the cost of a solution and the solution at the same time. Because sometime the cost function will change the solution, if it is changed, you should return the updated solution, other situations, just return the original one.

___

##### 通过模拟退火算法和遗传算法来实现一个类似StumbleUpon的网址推荐系统，模拟退火和遗传算法这里主要是为了优化解决NP难问题过程中暴力搜索解空间引入的性能问题
问题描述如下：   
* 用户A有一系列喜好关键词列表，不同关键词权重不同，和喜好程度成反比  
* 我们有一个网站列表，这些网站被不同的关键词所标注
* 我们要为用户A推荐X个网址，需要使用户A的满意度尽可能的大   

>optimization.py是优化算法库，里面实现了模拟退火和遗传算法（可灵活扩展增加优化函数）.如果想使用这个库解决问题，这个问题必须符合如下形式:   

* 解空间能用数字列表表示
* 解空间能被转化成一个成本值（通过一个成本函数，计算给定解空间需要耗费的成本）,以方便优化算法来对解空间进行合理取舍
* 成本函数必须返回当前解空间的成本值和解空间，因为有些成本函数会修改解空间（不允许出现重复数字的解空间，这时候如果出现重复则会将重复的数字替换为未被使用的），如果成本函数修改了解空间，返回修改后的，否则返回原始解空间即可
