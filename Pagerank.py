import json
import os
import networkx as nx


class Pagerank:
    def __init__(self):
        # 创建有向图
        self.G = nx.DiGraph()
        # 设置文件夹的路径
        self.path = 'D:/PythonCode/搜索引擎_data/participle_file/'
        # 获取文件夹中的文件数量
        self.length = len(os.listdir(self.path))
        # 打印文件数量
        print('在' + self.path + '文件夹下，共有' + str(self.length) + '份文件')
        # 调用创建正排表的方法
        self.compute_pagerank()

    def compute_pagerank(self):
        # 用一个变量来记录文件的序号
        count = 1
        location = {}
        # 遍历文件夹中的每个文件
        print('开始计算PageRank')
        for file in os.listdir(self.path):
            print(file)
            try:
                # 读取 JSON 文件
                with open(self.path + file, "r", encoding='utf-8') as f:
                    data = json.load(f)

                # 添加节点
                url = data["url"]
                self.G.add_node(url)

                # 添加边
                urls = data["urls"]
                for dst in urls:
                    self.G.add_edge(url, dst)
                location[count] = file
                count += 1
            except :
                print('error, 跳过此文件！')

        # 计算 PageRank
        pagerank = nx.pagerank(self.G)

        print('开始保存PageRank')
        count = 0
        # 更新每个节点的 PageRank 值并保存到文件中
        for url, value in pagerank.items():
            print(count)
            count += 1
            try:
                # 读取 JSON 文件
                with open(self.path + location[count], "r", encoding='utf-8') as f:
                    data = json.load(f)

                # 更新 PageRank 值并删除 urls
                data["pagerank"] = value
                # del data["urls"]

                # 保存更新后的数据到文件中
                with open(self.path + location[count], "w", encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            except:
                print('error, 保存数据失败！')

pagerank = Pagerank()
pagerank.compute_pagerank()