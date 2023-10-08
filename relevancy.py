from typing import List
import pandas as pd
from visualization.SearchResult import SearchResult
import math


class Relevancy:
    def __init__(self, search_results: List[SearchResult], query_words: List[str]):
        self.wij = None
        self.idf = None
        self.dictionary = None
        self.doc_ids = None  # 文档id
        self.search_results = search_results
        self.query_words = query_words

        self.compute_tf()
        self.build_dictionary()
        self.compute_idfj_and_tfidf()

    def build_dictionary(self):  # 构建词典
        self.dictionary = {}
        self.idf = {}
        for word in self.query_words:
            self.dictionary[word] = {}
            self.idf[word] = 0.0
            for doc_id in self.doc_ids:
                self.dictionary[word][doc_id] = 0

    def compute_tf(self):  # 词项j在文档i中的频率
        self.doc_ids = set()
        for doc in self.search_results:
            self.doc_ids.add(doc.id)
            df = pd.read_csv(f'D:/PythonCode/搜索引擎_data/forward_file/{doc.id}.csv', header=None)
            words_sum = df.iloc[:, 1].sum()  # 得到该文档的所有词数

            doc.tf = doc.count / words_sum  # 计算词频

    def compute_idfj_and_tfidf(self):  # 词项j的反文档频率= log2 (N/ dfj)
        for doc in self.search_results:
            doc.idfj = math.log(len(self.doc_ids) / doc.dfj)  # 词项j的反文档频率
            self.idf[doc.word] = doc.idfj
            doc.tfidf = doc.dfj * doc.idfj  # 计算tfidf
            self.dictionary[doc.word][doc.id] = doc.tfidf

    def compute_query_wij(self):  # 计算搜索词的wij
        self.wij = {}
        for word in self.query_words:
            tf = 1 / len(self.query_words)  # 计算词频
            idf = self.idf[word]  # 获取对应的逆文档频率
            self.wij[word] = tf * idf

    def compute_relevance(self):
        self.compute_query_wij()
        for doc in self.search_results:
            doc_den = 0  # 文档分母
            query_den = 0  # 查询词分母
            molecule = 0  # 分子
            for word in self.query_words:
                wij = self.wij[word]  # 获取搜索词的权重
                tfidf = self.dictionary[word][doc.id]  # 获取文档的tf-idf值
                if tfidf != 0:
                    has_query_word = True
                    doc_den += tfidf ** 2
                    query_den += wij ** 2
                    molecule += wij * tfidf  # 计算分子
            if doc_den != 0 and query_den != 0:
                doc.relevance = molecule / (doc_den ** 0.5 * query_den ** 0.5)   # 将计算得到的相关度值赋给文档对象的relevance属性
            else:
                doc.relevance = 0

