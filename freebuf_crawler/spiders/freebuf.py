# -*- coding: utf-8 -*-

import scrapy
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath('.'), 'freebuf_crawler'))

from freebuf_crawler.items import FreebufCrawlerItem

class FreebufSpider(scrapy.Spider):
    name = 'freebuf'
    allowed_domains = ['freebuf.com']
    start_urls = ['https://www.freebuf.com/page/573']
    base_url = 'https://www.freebuf.com/'
    page_url = 'https://www.freebuf.com/page/'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response: scrapy.http.Response):
        news_divs = response.xpath("//div[contains(@class, 'news-info')]")
        if not news_divs:
            return
        has_new_news = False
        for news_div in news_divs:
            item = self._parse_news_info(news_div)
            uri = item.get('url').replace(self.base_url, '')
            if not self.state.get(uri):
                self.state.setdefault(uri, True)
                has_new_news = True
                yield item
        # go to next page
        if has_new_news:
            cur_page_no = int(response.url.split('/')[-1])
            next_url = f"{self.page_url}{cur_page_no+1}"
            yield response.follow(url=next_url, dont_filter=False, callback=self.parse)

    def _parse_news_info(self, news_div):
        title = news_div.xpath("dl/dt/a/@title").extract_first().strip()
        url = news_div.xpath("dl/dt/a/@href").extract_first().strip()
        time_str = news_div.xpath(
            "dl/dd/span[@class='time']/text()").extract_first().strip()
        level = self.__parse_level(news_div)
        num_look = news_div.xpath(
            "div[@class='news_bot']/span[@class='look']/strong/text()").extract()[0].strip()
        num_comment = news_div.xpath(
            "div[@class='news_bot']/span[@class='look']/strong/text()").extract()[-1].strip()
        author = news_div.xpath(
            "dl/dd/span[contains(@class, 'name')]/a/text()").extract_first()
        if not author:
            author = news_div.xpath(
            "dl/dd/span[contains(@class, 'name')]/text()").extract_first()
        author = author.strip()
        tags = news_div.xpath(
            "div[@class='news_bot']/span[@class='tags']/a/text()").extract()
        text = news_div.xpath(
            "dl/dd[@class='text']/text()").extract_first().strip()

        item = FreebufCrawlerItem(
            title=title,
            url=url,
            time=time_str,
            level=level,
            num_look=int(num_look),
            num_comment=int(num_comment),
            author=author,
            tags=tags,
            text=text,
        )
        return item

    def __parse_level(self, news_div):
        if news_div.xpath(".//img[@title='现金奖励']").extract_first():  # 现金奖励
            level = '现金奖励'
        elif news_div.xpath(".//img[@title='金币奖励']").extract_first():
            num_coins = news_div.xpath(
                "//img[@title='金币奖励']/following-sibling::span/strong/text()").extract_first().strip()
            level = '金币' + num_coins
        # 红色标题
        elif news_div.xpath("dl/dt/a[@title and @style='color:#ED4747']").extract_first():
            level = '红色标题'
        else:
            level = ''
        return level


if __name__ == '__main__':

    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess(
        {
            'JOBDIR': 'freebuf_crawler/jobs/job-2',
        }
    )

    process.crawl(FreebufSpider)
    process.start()
