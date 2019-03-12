# -*- coding: utf-8 -*-
import scrapy
from ..items import FinvestItem
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class JiemoduiSpider(scrapy.Spider):
    name = 'jiemodui'
    # allowed_domains = ['https://www.jiemodui.com']
    start_urls = ['https://www.jiemodui.com/T/21016.html']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def parse(self, response):
        titles = response.xpath('//dd/p/a/text()').extract()
        links = ['https://www.jiemodui.com' + link for link in response.xpath('//dd/p/a/@href').extract()]
        for link in links:
            yield scrapy.Request(link, callback=self.news_parse, headers=self.headers)

    def news_parse(self, response):
        item = FinvestItem()
        client = MongoClient()
        db = client['Spider']
        coll = db.finvest

        if coll.find_one() is not None:
            if coll.find_one()['title'] == response.xpath('//h1[@name="name"]/text()').extract_first():
                raise CloseSpider("Duplicate Data")
        item['title'] = response.xpath('//h1[@name="name"]/text()').extract_first()
        item['create_time'] = response.xpath('//time/text()').extract_first()
        item['link'] = response.url
        item['content'] = response.xpath('string(//article[@class="content"])').extract_first()
        item['source'] = response.xpath('//div[@class="newContent"]/p/a/text()').extract_first()
        yield item
