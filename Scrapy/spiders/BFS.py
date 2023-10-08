import scrapy
import queue
import scrapy
from scrapy.linkextractors import LinkExtractor
import SPLIT

class BfsSpider(scrapy.Spider):   # 广度优先遍历
    name = "BFS"
    # allowed_domains = ["baike.baidu.com"]

    start_urls = ["https://news.sina.com.cn/"]
    count = 0
    queue = queue.Queue()
    split = SPLIT.split()
    def parse(self, response):
        link = LinkExtractor()
        links = link.extract_links(response)

        if response.headers.get("Content-Type", b"").startswith(b"text"):
            self.download(response,urls= [link.url for link in links])
        for i in links:
            self.queue.put(i)
        while not self.queue.empty():
            link = self.queue.get()
            yield scrapy.Request(url=link.url, callback=self.parse, encoding='utf-8')

    def download(self, response, urls):
        if response.text:
            self.count += 1
            print(self.count)

            title = response.xpath('./head[1]/title[1]/text()').extract_first()
            description = response.xpath('./head[1]/meta[@name="description"]/@content').extract_first()
            if self.split.get_text_and_participle(response.text, self.count, response.url, title, description, urls) == 1:
                self.count -= 1
