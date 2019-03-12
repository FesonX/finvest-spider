# -*- coding: utf-8 -*-
import scrapy

from ..items import FinvestItem
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class TrjcnSpider(scrapy.Spider):
    name = 'trjcn'
    start_urls = ['http://news.trjcn.com/list_70.html']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    count = 3

    def parse(self, response):
        data = response.xpath('//*[@id="wap_pager_data"]/li/div/a/@href')
        for link in data:
            yield scrapy.Request(link.extract(), callback=self.news_parse, headers=self.headers)

        if (self.count < 100):
            next_url = 'http://news.trjcn.com/list_70.html?page=%d' % self.count

            self.count = self.count + 1
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers, dont_filter=False)

    def news_parse(self, response):
        item = FinvestItem()
        client = MongoClient()
        db = client['Spider']
        coll = db.finvest

        if coll.find_one() is not None:
            if coll.find_one()['title'] == response.xpath('//div[@class="newDetail"]/h2/text()').extract_first():
                raise CloseSpider("Duplicate Data")
        item['title'] = response.xpath('//div[@class="newDetail"]/h2/text()').extract_first()
        item['create_time'] = response.xpath('//div[@class="fl"]/span[1]/text()').extract_first()
        item['link'] = response.url
        item['content'] = response.xpath('string(//div[@id="newDetailCont"])').extract_first().replace(u'\n\n\n\t', u'\n').strip()
        item['source'] = response.xpath('//div[@class="fl"]/span[2]/text()').extract_first()[3:]
        yield item
