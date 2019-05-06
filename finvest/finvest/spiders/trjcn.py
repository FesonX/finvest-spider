# -*- coding: utf-8 -*-
import scrapy

from ..items import FinvestItem
from scrapy import Request
from fake_useragent import UserAgent
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
import json
import time


class TrjcnSpider(scrapy.Spider):
    name = 'trjcn'
    start_urls = []
    for i in range(100):
        url = 'https://news.trjcn.com/rz/rongzikuaixun/?page=%d' % i
        start_urls.append(url)

    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agent': ua.random,
    }

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    # }
    count = 3

    def start_requests(self):
        for i in self.start_urls:
            yield Request(i, headers=self.headers)

    def parse(self, response):
        data = Selector(text=json.loads(response.body)['data']['html']).xpath('//li')
        for link in data.xpath('//div[@class="item-title"]/a/@href').extract():
            yield scrapy.Request(link, callback=self.news_parse, headers=self.headers)

    def news_parse(self, response):
        item = FinvestItem()
        # client = MongoClient()
        # db = client['Spider']
        # coll = db.finvest
        #
        # if coll.find_one() is not None:
        #     if coll.find_one()['title'] == response.xpath('//div[@class="newDetail"]/h2/text()').extract_first():
        #         raise CloseSpider("Duplicate Data")

        item['title'] = response.xpath('//h5/text()').extract_first()
        t = response.xpath('//div[@class="article-detail-time"]/text()').extract_first().replace('年', '-').replace('月', '-').replace('日', ' ')
        time_array = time.strptime(t, "%Y-%m-%d %H:%M")
        item['create_time'] = int(time.mktime(time_array))
        item['link'] = response.url
        item['content'] = response.xpath('string(//div[@class="article-detail-text"])').extract_first().replace('\n', ' ').replace('\t', ' ')
        item['source'] = response.xpath('//div[@class="article-detail-source"]/text()').extract_first().replace('信息来源：', '')
        yield item
