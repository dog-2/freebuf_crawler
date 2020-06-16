# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FreebufCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    level = scrapy.Field() # 现金奖励/金币+n/红色标题
    num_look = scrapy.Field()
    num_comment = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
    text = scrapy.Field()