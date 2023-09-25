# 导入所需的模块
import json
import os
import ast
import csv
import time


# 定义一个类来创建正排表
class Forward:
    path = ""

    # 初始化类的属性
    def __init__(self):
        # 设置文件夹的路径
        self.path = 'D:/PythonCode/搜索引擎_data/participle_file/'
        # 获取文件夹中的文件数量
        self.length = len(os.listdir(self.path))
        # 打印文件数量
        print('在' + self.path + '文件夹下，共有' + str(self.length) + '份文件')
        # 调用创建正排表的方法
        self.creat_forward()

    # 定义一个方法来创建正排表
    def creat_forward(self):

        # 用一个变量来记录文件的序号
        count = 0
        # 遍历文件夹中的每个文件
        for file in os.listdir(self.path):
            try:
                # 增加文件序号
                count += 1
                # 打印文件序号
                print(count)
                # 打开文件并读取内容
                with open(self.path + file, 'r', encoding='utf-8') as f:
                    doc = json.load(f, strict=False)
                # 将字符串转换为列表
                lt = ast.literal_eval(doc['text'])
                id = doc['id']
                # 用一个字典来存储正排表，键是单词，值是一个列表，列表中每个元素是一个元组，表示文档ID和位置
                location = {}
                word_count = {}
                # 用一个变量来记录位置
                position = 0
                # 遍历单词列表
                for word in lt:
                    # 增加位置
                    position += 1
                    # 如果单词不在正排表中，就初始化一个空列表作为值
                    if word not in location:
                        location[word] = []
                        word_count[word] = 0
                    # 将文档ID和位置作为一个元组添加到正排表中的列表里
                    location[word].append((int(id), position))
                    word_count[word] += 1
                # 将正排表写入csv文件中，每一行表示一个单词及其对应的文档ID和位置列表
                with open(f'D:/PythonCode/搜索引擎_data/forward_file/{id}.csv', 'w', encoding='utf-8-sig', newline='') as f :
                    writer = csv.writer(f)
                    for word, value in location.items():
                        writer.writerow([word, word_count[word], value])
            except:
                print('error, 跳过此文件！')


start = time.time()
# 创建一个类的实例，开始创建正排表
forword = Forward()
end = time.time()


