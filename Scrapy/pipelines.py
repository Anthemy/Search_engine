# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
from random import random

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyPipeline:
    # count = 0
    #
    # def open_spider(self, spider):
    #     # 在爬虫开启时执行一次
    #     self.count = 0  # 创建计数变量
    #
    # def process_item(self, item, spider):
    #     self.count += 1  # 计数加一
    #     # 处理每个item数据
    #     with open(f'./download_file/{self.count}.html', 'w', encoding='utf-8') as fp:  # 打开本地文件
    #         fp.write(f'id:{self.count},url={item["url"]},\\n')  # 写入url字段
    #         fp.write(item["text"])  # 写入text字段
    #     return
    #
    # def close_spider(self, spider):
    #     # 在爬虫关闭时执行一次
    #     print(self.count)  # 打印计数值
    def process_item(self, item, spider):

        return


