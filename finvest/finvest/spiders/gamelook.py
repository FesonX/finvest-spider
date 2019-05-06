# -*- coding: utf-8 -*-
import scrapy
import time
from ..items import FinvestItem
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class GamelookSpider(scrapy.Spider):
    name = 'gamelook'
    # allowed_domains = ['www.gamelook.com.cn']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    }

    count = 2

    # http://www.gamelook.com.cn/category/投资创业/风险资本合作
    start_urls = ['http://www.gamelook.com.cn/category/%E6%8A%95%E8%B5%84%E5%88%9B%E4%B8%9A/%E9%A3%8E%E9%99%A9%E6%8A%95%E8%B5%84%E8%B5%84%E6%9C%AC%E5%90%88%E4%BD%9C/']

    def parse(self, response):
        links = [link for link in response.xpath('//a[@class="thumb"]/@href').extract()]
        for link in links:
            yield scrapy.Request(link, callback=self.news_parse, headers=self.headers)

        if self.count < 100:
            next_url = "http://www.gamelook.com.cn/category/%E6%8A%95%E8%B5%84%E5%88%9B%E4%B8%9A/" \
                       "%E9%A3%8E%E9%99%A9%E6%8A%95%E8%B5%84%E8%B5%84%E6%9C%AC%E5%90%88%E4%BD%9C/page/" + str(self.count) + '/'
            self.count += 1
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers, dont_filter=False)

    def news_parse(self, response):
        item = FinvestItem()
        item['title'] = response.xpath('//h1[@class="entry-title"]/text()').extract_first()
        t = response.xpath('//div[@class="entry-info"]/span/text()').extract_first()
        time_array = time.strptime(t, "%Y-%m-%d")
        item['create_time'] = int(time.mktime(time_array))
        item['link'] = response.url
        item['content'] = response.xpath('string(//div[@class="entry"]/div[2])').extract_first()
        item['source'] = response.xpath('string(//div[@class="entry-copyright"]/p/span/text())').extract_first()
        if item['source'] == '':
            item['source'] = 'gamelook'
        yield item
