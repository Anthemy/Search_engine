import ast
import json
from temp.SearchResult import SearchResult
import pandas as pd
from SPLIT import split


class Search:

    results = []

    def __init__(self):
        self.where = None

    def receive_text(self, text):
        # st = split()
        self.text = text
        # self.text, self.keywords = st.participle(self.text)
        # self.text = ast.literal_eval(self.text)
        print(self.text)
        self.read_reverse()

    def read_reverse(self):  # 读取倒排表
        df = pd.read_csv("D:/PythonCode/搜索引擎_data/reverse_file/1.txt", header=None)
        df.columns = ['word', 'value']
        mask = df['word'] == self.text
        self.where = ast.literal_eval(df.loc[mask, 'value'].iloc[0])

        # print(where)

    def find_file(self):  # 找到文件
        loction = {}
        for item in self.where:
            if item[0] not in loction:
                loction[item[0]] = []
            loction[item[0]].append(item[1])
        # print(loction)
        for item in loction:
            print(item)
            with open(f"D:/PythonCode/搜索引擎_data/participle_file/{item}.txt", 'r', encoding='utf-8') as fp:
                doc = json.load(fp, strict=False)
                self.results.append(SearchResult(doc['url'], doc['title'], doc['description']))
        return self.results


# search = Search()
# search.receive_text('中文')
# search.find_file()
