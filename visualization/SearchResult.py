class SearchResult:

    tf = None # tf 是相关度计算中的一部分，是词项j在文档i中的频率
    dfj = None # dfj 是词项j的文档频率= 包含词项j的文档数量，也就是doc_count
    idfj = None # idfj 是词项j的反文档频率= log2 (N/ dfj)  N: 文档集中文档总数
    tfidf = None
    similarity = None # 相关度
    words = None # 包含文档中的所有词
    relevance = None # 相关度
    def __init__(self, id, word, url, title, summary, count, pagerank, doc_count):
        self.id = id
        self.word = word
        self.url = url
        self.title = title
        self.summary = summary
        self.count = count
        self.pagerank = pagerank
        self.dfj = doc_count      # 与这个搜索结果有关， 是含有该搜索词的文档数， 放在这里方便计算


    def __repr__(self):
        return 'id: ' + str(
            self.id) + ', word: ' + self.word + ', url: ' + self.url + ', title: ' + self.title + ', summary: ' + self.summary + ', count: ' + str(
            self.count) + ', pagerank: ' + str(self.pagerank)

    def __str__(self) -> str:
        return 'id: ' + str(
            self.id) + ', word: ' + self.word + ', url: ' + self.url + ', title: ' + self.title + ', summary: ' + self.summary + ', count: ' + str(
            self.count) + ', pagerank: ' + str(self.pagerank)

    def set_score(self,score):
        self.score = score