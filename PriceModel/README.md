#####This case includes more than one algorithm to build price model for iphone5

* get_ganji.py is the crawler to get the iphone5 price information of bj.ganji.com. It cleaning the data too
* iphone5_price_model.py is responsible for preprocessing the data and invoking decision tree algorithm and drawing dendrogram.
* numpredict.py is the algorithm lib
* optimization.py is the optimization algorithm occured before the time, but we modify it to suit for this case
* source data is inclusive under the data directory 

___

#####本案例综合了多重算法来构建商品的价格模型

* get_ganji.py负责从赶集网抓取二手iphone5的售价信息并对获取到的数据进行清洗
* iphone5_price_model.py读入源数据，调用相关算法对测试数据进行预测，绘制价格分布图
* numpredict.py包含相关算法和绘图函数
* optimization.py是之前案例出现过的优化算法库，但是为了适应本案例的问题进行了一些修改
* 源数据均在data目录下

___

#####Blog
[http://zuojie.github.io/2013/10/11/机器学习实践%3A土豪们的最爱-为二手iphone5构建价格模型.html](http://zuojie.github.io/demo/dt/desicion_tree_100.jpg)
