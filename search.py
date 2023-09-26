import ast
import json
from visualization.SearchResult import SearchResult
import pandas as pd
from SPLIT import split
from relevancy import Relevancy
class Search:
    results = []

    def __init__(self):
        self.where = None

    def receive_text(self, text):       # 接收搜索词
        st = split()
        self.text = text
        self.text, self.keywords = st.participle(self.text)     # 获取搜索语句分词结果以及关键词
        self.text = ast.literal_eval(self.text)
        print('keywords', self.keywords)
        print('text', self.text)
        self.read_reverse()

    def read_reverse(self):  # 读取倒排表
        df = pd.read_csv("D:/PythonCode/搜索引擎_data/reverse_file/1.txt", header=None)
        df.columns = ['word', 'value']
        self.results = []
        for text in self.text:
            mask = df['word'] == text
            try:
                self.where = ast.literal_eval(df.loc[mask, 'value'].iloc[0])
                reslut = self.find_file(text)
                if reslut:
                    self.results.extend(reslut)
            except:
                print('没有此词！')
                self.where = []
        # self.sort_results()
        # print(self.results)

    def find_file(self, text):  # 找到文件
        loction = {}
        for item in self.where:
            if item[0] not in loction:
                loction[item[0]] = []
            loction[item[0]].append(item[1])
        # print(loction)
        result = []
        doc_len = len(loction)      # 文档数
        for key, value in loction.items():
            # print(key)
            try:
                with open(f"D:/PythonCode/搜索引擎_data/participle_file/{key}.txt", 'r', encoding='utf-8') as fp:
                    doc = json.load(fp, strict=False)
                    result.append(SearchResult(key, text, doc['url'], doc['title'], doc['description'], len(value),
                                               doc['pagerank'], doc_len))
                    print(result[len(result) - 1])
            except Exception as e:
                print(e.args)
        return result

    flag = {}
    def get_score(self, result):  # 定义一个计算搜索结果得分的函数，它接受一个搜索结果和一个关键词列表作为参数
        score = 0  # 初始化得分为0
        # 遍历每个关键词
        for word in self.text:
            # 如果搜索结果的标题中包含关键词，得分加10
            if word in result.title:
                score += 50
            # 如果搜索结果的摘要中包含关键词，得分加5
            if word in result.summary:
                score += 25
        if result.word in self.keywords:  # 如果搜索结果的词在选出的关键词中， 得分加5
            score += 15
        score += result.count * 15  # 得分加5*网页含搜索词数
        score += result.relevance*10000000
        if result.id in self.flag:  # 要是在别的搜索词中出现过该文档，则得分加8*出现次数
            score += 8*self.flag[result.id]
            self.flag[result.id] += 1
        else:
            self.flag[result.id] = 1

        # print('id: ' + str(result.id), ' score: ' + str(score))
        # 返回得分
        result.set_score(score)
        return score

    def remove_duplicates(self, key):       # 排序函数之一
        seen = set()
        return [x for x in self.results if getattr(x, key) not in seen and not seen.add(getattr(x, key))]

    # 定义一个排序函数
    def sort_results(self):
        relev = Relevancy(self.results,self.text)
        relev.compute_relevance()

        # 对搜索结果列表按照得分降序排序，并返回排序后的列表
        self.results = sorted(self.results, key=lambda result: self.get_score(result), reverse=True)
        self.results = self.remove_duplicates(key='id')

        return self.results

# search = Search()
# search.receive_text('GitHub怎么上传代码')

