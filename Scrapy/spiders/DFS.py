import scrapy
from scrapy.linkextractors import LinkExtractor

import SPLIT
from Scrapy.items import ScrapyItem


class DfsSpider(scrapy.Spider):
    name = "DFS"
    # allowed_domains = [r"*"]
    start_urls = ["https://baike.baidu.com"]
    count = 0

    split = SPLIT.split()

    def parse(self, response):  # 深度优先遍历
        if not response.headers.get("Content-Type", b"").startswith(b"text"):
            return
        link = LinkExtractor()
        links = link.extract_links(response)
        # item = ScrapyItem() # 创建一个WebPageItem对象
        # item["url"] = response.url # 将响应的url赋值给item的url字段
        # item["text"] = response.text # 将响应的文本赋值给item的text字段
        # yield item # 返回item对象
        self.download(response, urls=[link.url for link in links])
        for link in links:
            if not response.headers.get("Content-Type", b"").startswith(b"text"):
                return
            yield scrapy.Request(url=link.url, callback=self.parse, encoding='utf-8')

    def download(self, response, urls):
        if response.text:
            self.count += 1
            print(self.count)


            title = response.xpath('./head[1]/title[1]/text()').extract_first()
            description = response.xpath('./head[1]/meta[@name="description"]/@content').extract_first()
            if self.split.get_text_and_participle(response.text, self.count, response.url, title, description, urls) == 1:
                self.count -= 1


