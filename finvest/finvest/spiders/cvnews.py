# -*- coding: utf-8 -*-
import scrapy
import time
import json

from scrapy import Request
from ..items import FinvestItem
from pymongo import MongoClient
from scrapy.exceptions import CloseSpider


class CvnewsSpider(scrapy.Spider):
    name = 'cvnews'
    allowed_domains = ['www.chinaventure.com.cn']
    start_urls = ['https://www.chinaventure.com.cn/cmsmodel/news/jsonListByEvent/0-100.do']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_request(self):
        yield Request(self.start_urls, headers=self.headers)
    
    def time_convertor(self, time_num):
        time_struct = time.localtime(float(time_num/1000))
        return time.strftime("%Y-%m-%d %H:%M:%S", time_struct)

    def parse(self, response):
        item = FinvestItem()
        sites = json.loads(response.body_as_unicode())

        for i in sites['data']:
            client = MongoClient()
            db = client['Spider']
            coll = db.finvest

            if(coll.find_one() is not None):
                if (coll.find_one()['title'] == i['news']['title']):
                    raise CloseSpider("Duplicate Data")
            item['link'] = "https://www.chinaventure.com.cn/cmsmodel/news/detail/%s.shtml" % (i['news']['id'])
            item['title'] = i['news']['title']
            item['source'] = i['news']['srcName']
            item['create_time'] = self.time_convertor(i['news']['publishAt'])
            item['content'] = i['news']['content']
            yield item