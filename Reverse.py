import ast

import pandas as pd
import os
import csv


class Reverse:
    path = ""

    # 初始化类的属性
    def __init__(self):
        # 设置文件夹的路径
        self.path = 'D:/PythonCode/搜索引擎_data/forward_file/'
        # 获取文件夹中的文件数量
        self.length = len(os.listdir(self.path))
        # 打印文件数量
        print('在' + self.path + '文件夹下，共有' + str(self.length) + '份文件')
        # 调用创建正排表的方法
        self.creat_reverse()

    def creat_reverse(self):
        count = 0
        word_index = {}
        for file in os.listdir(self.path):
            try:

                count += 1
                print(file)

                df = pd.read_csv(self.path + file, header=None)
                df.columns = ['word', 'count', 'location']  # 转换化成datafram，为列命名
                # print(df)

                def get_word(row):
                    # print('=' * 100)
                    # print(row)
                    word = row['word']
                    location = row['location']
                    if word not in word_index:
                        word_index[word] = []

                    word_index[word].extend(ast.literal_eval(location))
                    # print(word_index[word])

                df.apply(get_word, axis=1)
                if count == 7000:
                    break

            except:
                print('error, 跳过此文件！')
        with open(f'D:/PythonCode/搜索引擎_data/reverse_file/1.txt', 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            for word, value in word_index.items():
                writer.writerow([word, value])


reverse = Reverse()
