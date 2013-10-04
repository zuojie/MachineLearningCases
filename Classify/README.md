###Classifying Intelligence can help us filter spam mail, classify document automatically etc
This case is use classifying algorithm(NaiveBayes & Fisher Method) to classify blogs, which is a match about [ACMer blog classify]("http://acmicpc.info/archives/1194")
* classify.py is the classifying algorithm lib
* blog_classify.py is the main script, response for preprocessing data, training classify data, making classify etc
* merge_blog_title.py is a helper script
* ./data/blog_title.txt is the training dataset
* ./data/final_blog_title.txt is the test dataset
* ./data/final_result.txt is the benchmark result, come from [here]("http://blog.acmicpc.info/compare/result.html")
* ./data/bayes_classify.txt is the result of naivebayes classifying algorithm
* ./data/fisher_classify.txt is the result of fisher method 
* ./jieba/ and ./extra_dict/ is a [Python Chinese segmentation module]("https://github.com/fxsjy/jieba") used in my code
