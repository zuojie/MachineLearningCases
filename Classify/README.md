###Classifying Intelligence can help us filter spam mail, classify document automatically etc
This case is use classifying algorithm(NaiveBayes & Fisher Method) to classify blogs, which is a match about [ACMer blog classify](http://acmicpc.info/archives/1194)
* classify.py is the classifying algorithm lib
* blog_classify.py is the main script, response for preprocessing data, training classify data, making classify etc
* merge_blog_title.py is a helper script
* ./data/blog_title.txt is the training dataset
* ./data/final_blog_title.txt is the test dataset
* ./data/final_result.txt is the benchmark result, come from [here](http://blog.acmicpc.info/compare/result.html)
* ./data/bayes_classify.txt is the result of naivebayes classifying algorithm
* ./data/fisher_classify.txt is the result of fisher method 
* ./jieba/ and ./extra_dict/ is a [Python Chinese segmentation module](https://github.com/fxsjy/jieba) used in my code

___

这个机器学习的案例是采用朴素贝叶斯和费舍尔方法分类算法对一系列博客进行分类，题目源于一个[比赛](http://acmicpc.info/archives/1194).
比赛提供一些没有标记的训练数据，需要我们先基于规则的方法来进行预处理标记，这个方法来自[康师傅](http://www.bottomcoder.ru/wordpress/archives/78#comment-136).抛开细节不说，正规军都是用博客的摘要和正文来进行训练的，我直接偷懒使用了博客标题来进行训练
和最终的测试，结果见相关文件，马马虎虎差强人意吧。目前成绩最好的是康师傅的88%左右的误差记录。各文件功能性说明见上，不在赘述。
