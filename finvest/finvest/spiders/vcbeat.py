# -*- coding: utf-8 -*-
import scrapy

from ..items import FinvestItem
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider
import json


class VcbeatSpider(scrapy.Spider):
    name = 'vcbeat'
    start_urls = ['http://vcbeat.top/Index/Index/ajaxGetArticleList']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    count = 2

    def parse(self, response):
        data = json.loads(response.body_as_unicode())['data']
        links = ["https://vcbeat.net/" + link['detail_id'] for link in data]
        for link in links:
            yield scrapy.Request(link, callback=self.news_parse, headers=self.headers)

        if self.count < 51:
            next_url = "http://vcbeat.top/Index/Index/ajaxGetArticleList?page=%d" % self.count
            self.count += 1
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers, dont_filter=False)

    def news_parse(self, response):
        item = FinvestItem()
        client = MongoClient()
        db = client['Spider']
        coll = db.finvest

        if coll.find_one() is not None:
            if coll.find_one()['title'] == response.xpath('//p[@class="tle"]/text()').extract_first():
                raise CloseSpider("Duplicate Data")
        item['title'] = response.xpath('//p[@class="tle"]/text()').extract_first()
        item['create_time'] = response.xpath('//span[@class="time"]/text()').extract_first()
        item['link'] = response.url
        item['content'] = response.xpath('string(//div[@class="art_text"])').extract_first()
        item['source'] = response.xpath('//span[@class="name"]/text()').extract_first()
        yield item
