# 2 使用大模型 做路由层

{"方向1":{'小方向1':'',
           '小方向2':"",
       "如何解决河道问题":"",}
"方向2":}

方法
类似github 分支 分支与合并的关系
1 - 2    - 3   - 4
  \ 2-1  \ 3-1
  \ 2-2/ \ 3-2

使用树的数据结构, 并进行串联



概念

什么是河道:
河道: 1  2  3  4  5
     11 22 33 44 55



# client

1 抽取出这些文件

2 经过路由层

路由层 ----> 

# queryer

3 对于经过路由层处理归类好的文章进行合并

4 对初始化的文章结构采用合并的策略

5 对于添加动作, 则是维持之前的决策结构不大变化, 而微调其结构

6 是否验证的标签, 这很重要 未来还可以加入概率或者神经网络方式



7 调用 TODO 然后再说


from article_forestz import MyLocalLLMClient,MyArticleDecisionMaker,ArticleForest


# For local testing, using a simpler model or mock:
my_llm_client = MyLocalLLMClient(
    model_name="gemini-2.5-flash-preview-04-17-nothinking"
)  
my_decision_maker = MyArticleDecisionMaker(llm_client=my_llm_client)
article_forest = ArticleForest(article_decision_maker=my_decision_maker)

inputs = [{"id": "Init1", "content": text1},
 {"id": "Init2", "content": text2},
 {"id": "Init3", "content": text3}]

article_forest.build_initial_forest(inputs)

article_forest.print_tree()
article_forest.export_graphviz()

new_articles = [
        {"id": "NewA1", "content": test4}, # 归入AI类，可能作为新子层
]

for article in new_articles:
    article_forest.add_article(article["content"], article["id"])
    