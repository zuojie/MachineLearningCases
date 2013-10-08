#####Decision Tree can help us predict someting like price, user action and tomorrow's weather etc, if you give it enough information. Actually, with enough information, it can almost predict anything,  pretty a cool thing, aha. Here comes the relevant case: predict Beijing's house rental by means of decision tree algorithm.

* decisiontree.py is the decision tree algorithm lib, including function to visualitions of the decision tree  
* get_ganji_dat.py is the crawler to get the house rent information of bj.ganji.com and cleaning the data
* ganji_house_rent_price_predict.py is responsible for preprocessing the data and invoking decision tree algorithm and drawing dendrogram.
* source data is inclusive under the data directory 
* img contains the decision tree training result with different datasets
* Fonts file is to solve the gibberish problem when PIL displays Chinese

___

#####如果我们提供足够丰富的信息，决策树算法可以帮助我们预测商品价格，用户行为，甚至明日天气等。事实上，在获得足够相关信息之后，决策树算法可以对任何事情做出基于概率的预测。是一个很酷的算法！

* decisiontree.py 是决策树算法库，还包括绘制决策树的功能函数
* get_ganji_dat.py负责爬取赶集网北京站租房相关的数据，并进行预清洗
* ganji_house_rent_price_predict.py负责预处理数据，并调用决策书算法进行训练生成决策树，然后调用绘制出图的函数
* 源数据均在data目录下
* img目录包含了不同数据集规模下生成的相应的决策树，包括剪枝的和未剪枝的
* 字体文件是为了解决PIL显示中文的乱码问题

___

#####Appendix
![100](http://zuojie.github.io/demo/dt/desicion_tree_100.jpg)
