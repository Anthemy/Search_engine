import ast
import json
from visualization.SearchResult import SearchResult
import pandas as pd
from SPLIT import split
from relevancy import Relevancy
import re
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
        max_length = 80  # 设置摘要的最大字符数
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
                    # print(type(key))
                    with open(f"D:/PythonCode/搜索引擎_data/Original_text/{key}.txt", 'r', encoding='utf-8') as f:
                        Original_text = f.read()
                        # contents = Original_text['content']
                        # print(11)
                    summary = doc['description'] if text in doc['description'] else self.keyword_matching_summary(Original_text, self.text, doc['title'])
                    # 如果摘要字符数超过了最大限制，则截断文本
                    if len(summary) > max_length:
                        summary = summary[:max_length] + '...'
                    result.append(SearchResult(key, text, doc['url'], doc['title'],summary, len(value),
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
        score += result.relevance*1e7
        score += result.pagerank*1e5
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

    def keyword_matching_summary(self, contents, keywords, title):
        sentences = contents.split('。')  # 将文本按句子分割成列表
        summary_sentences = []
        for i in range(len(sentences)):
            if any(keyword in sentences[i] for keyword in keywords):
                # 截取包含关键词的句子
                start_index = max(0, i)  # 关键词前5个句子作为开头
                end_index = min(i + 1, len(sentences))  # 关键词后6个句子作为结尾
                if title not in sentences[start_index:end_index]:
                    summary_sentences.append(sentences[start_index:end_index])

        # summary = '. '.join(summary_sentences)
        summary = " ".join('%s' %a for a in summary_sentences)
        summary = summary.replace('[', '').replace("'", '').replace(']', '')
        return summary
        # corpus=[]

        window_size=20
        # print(contents)
        # corpus.append(contents)  # 将 contents 直接添加到 corpus 中
        # doc_ids.append(i)
        # sentences = contents.split()  # 按空格切分句子
        # sentences = "".join(sentences)  # 将句子列表合并为字符串
        # print(sentences)
        # sentences = re.split(' ', contents)
        # keyword_counts = []
        # # summaries=[]
        # # 在句子列表上进行滑动窗口操作
        # for j in range(len(sentences) - window_size + 1):
        #     window = sentences[j: j + window_size]
        #     keyword_count = sum([1 for sentence in window if any(word in sentence for word in keywords)])
        #     keyword_counts.append(keyword_count)
        #
        #     # 根据投票方式选择关键词数量最多的窗口
        #     max_count = max(keyword_counts)
        #     max_index = keyword_counts.index(max_count)
        #     # 删除英文字符的正则表达式模式
        #     # pattern = re.compile(r'[a-zA-Z]')
        #     # 原始的summary字符串
        #     summary = ''.join(sentences[max_index: max_index + window_size])
        #     # 删除英文字符后的summary字符串
        #     # clean_summary = re.sub(pattern, '', summary)
        # return summary

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

