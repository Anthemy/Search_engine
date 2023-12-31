import os
from bs4 import BeautifulSoup
import jieba
import jieba.analyse
import pandas as pd
from simhash import Simhash


class split:

    sim = []  # 保存网页的simhash

    def participle(self,text):

        # print(text)
        keywords = jieba.analyse.extract_tags(text, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))

        text = jieba.lcut_for_search(text)
        text = pd.Series(text)[pd.Series(text).apply(len) > 0]  # 去除长度为0的词

        stopwords = ['，', '。', '！', '？', '、', '；', '：', '“', '”', '‘', '’', '（', '）', '【', '】', '{', '}', '<',
                     '>', '《', '》', '『', '』', '「', '」', '[', ']', '—', '——', '-', '_', '~', '@', '#', '$', '\n',
                                                                                                           '%', '^',
                     '&', '*', '(', ')', '+', '=', '|', '/', '`', '.', ',', '·', '\xa0', '\t', '\u3000', '\r', '\u200b',
                                                                                                         ' ', ':', ';',
                     '\\', '...', '▪', "'", '"', '!', '了', '的', '啊', '哎', '哎呀', '哎哟', '唉', '嗄', '嗯',
                     '嘛', '呀', '呃', '呦', '哈', '哈哈', '嘿', '嘿嘿', '喂', '嗨', '哇', '哇塞', '哇哦', '哦',
                     '噢', '欸', '诶', '诶嘿', '额', '额滴', '呜', '呜呼', ' ', '\ue610', '\ufeff', '\xa0']

        return str(text[~text.isin(stopwords)].tolist()), keywords

    def get_text_and_participle(self, text, count, url, title, description, urls):
        soup = BeautifulSoup(text, "html.parser")
        Original_text = soup.get_text()
        Original_text = Original_text.replace("\n", "").replace('\r', '').replace('\t', '').replace('\u3000','')
        # print(text)
        text, keywords = self.participle(Original_text)
        if self.page_review(text) == 1:
            return 1
        with open(f'D:/PythonCode/搜索引擎_data/participle_file/{count}.txt', 'w', encoding='utf-8') as f:
            f.write(f'{{"id": "{count}", "url": "{url}", "title": "{title}", "description": "{description}", '
                    f'"keywords": "{keywords}", "text": "{text}", "urls": "{urls}"}}')
        with open(f'D:/PythonCode/搜索引擎_data/Original_text/{count}.txt', 'w', encoding='utf-8') as f:
            f.write(Original_text)
        return 0

    def page_review(self, text):
        simhash1 = Simhash(text)
        for hash in self.sim:
            # print("海明距离：",simhash1.distance(hash)/len(text))
            if simhash1.distance(hash) < 10:
                # print(text)
                return 1
        self.sim.append(simhash1)
        return 0
