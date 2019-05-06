# -*- coding: utf-8 -*-
import scrapy
from ..items import FinvestItem
import time
from fake_useragent import UserAgent
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class JiemoduiSpider(scrapy.Spider):
    name = 'jiemodui'
    # allowed_domains = ['https://www.jiemodui.com']
    start_urls = ['https://www.jiemodui.com/T/21016.html']

    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random,
    }

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # }

    def parse(self, response):
        titles = response.xpath('//dd/p/a/text()').extract()
        links = ['https://www.jiemodui.com' + link for link in response.xpath('//dd/p/a/@href').extract()]
        for link in links:
            yield scrapy.Request(link, callback=self.news_parse, headers=self.headers)

    def news_parse(self, response):
        item = FinvestItem()
        # client = MongoClient()
        # db = client['Spider']
        # coll = db.finvest

        # if coll.find_one() is not None:
        #     if coll.find_one()['title'] == response.xpath('//h1[@name="name"]/text()').extract_first():
        #         raise CloseSpider("Duplicate Data")
        item['title'] = response.xpath('//h1[@name="name"]/text()').extract_first()
        t = response.xpath('//time/text()').extract_first()
        time_array = time.strptime(t, "%Y-%m-%d %H:%M")
        item['create_time'] = int(time.mktime(time_array))
        item['link'] = response.url
        item['content'] = response.xpath('string(//article[@class="content"])').extract_first().replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
        item['source'] = response.xpath('//div[@class="newContent"]/p/a/text()').extract_first()
        if item['source'] == '':
            item['source'] = '芥末堆'
        yield item
