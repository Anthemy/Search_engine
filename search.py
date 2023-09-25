import ast

import pandas as pd
from SPLIT import split


class Search:

    def __init__(self):
        st = split()
        self.text = input("请由此输入：")
        self.text, self.keywords = st.participle(self.text)
        print(self.text)
        self.read_reverse()


    def read_reverse(self):  # 读取倒排表
        df = pd.read_csv("D:/PythonCode/搜索引擎_data/reverse_file/1.txt", header=None)
        df.columns = ['word', 'value']

        print(df.where(df['word'] == input).dropna()['value'].tolist())
        print(type(df.where(df['word'] == input).dropna()['value'].tolist()))
        # return ast.literal_eval(df.where(df['word'] == input).dropna()['value'])



search = Search()
