# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FreebufCrawlerPipeline(object):
    def process_item(self, item, spider):
        item.setdefault(
            'tags', 
            ['|'.join('tags') for tag in item.get('tags')]
        )
        return item
