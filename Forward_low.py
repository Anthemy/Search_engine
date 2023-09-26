import json
import pandas as pd
import os
import time

class Forward:
    count = 0
    length = 0
    index = 0

    def __init__(self):
        path = 'D:/PythonCode/搜索引擎_data/participle_file/'
        self.length = len(os.listdir(path))
        print('在' + path + '文件夹下，共有' + str(self.length) + '份文件')
        self.creat_forward()

    def creat_forward(self):
        while self.count <= self.length:
            self.count += 1
            print(self.count)
            # try:
            doc = json.load(
                open(f'D:/PythonCode/搜索引擎_data/participle_file/{self.count}.txt', 'r', encoding='utf-8'),
                strict=False)

            lt = eval(doc['text'])      # 将词提取出来

            df = pd.DataFrame(lt)
            df.columns = {'word'}       # 转换化成datafram，为列命名

            df1 = df.groupby('word').size().reset_index(name='count')   # 分组

            df = pd.merge(df, df1, how='left', on='word')

            df['location'] = '0'

            # print(df)

            def find_location(word):
                index = df.index[df['word'] == word].tolist()
                # print(index)
                df.loc[index, 'location'] = str(index)

            df1['word'].apply(find_location)
            df = df.groupby(['word', 'location', "count"]).size().reset_index(name='visualization')

            df.drop('visualization', axis=1, inplace=True)
            df.to_csv(f'D:/PythonCode/搜索引擎_data/forward_file/{self.count}.txt', index=False)


start = time.time()
# 创建一个类的实例，开始创建正排表
forword = Forward()
end = time.time()

print("总时间："+str(end-start))
