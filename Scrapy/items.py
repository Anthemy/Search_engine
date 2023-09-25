# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyItem(scrapy.Item):
    url = scrapy.Field()  # 网页链接
    text = scrapy.Field()  # 网页源代码