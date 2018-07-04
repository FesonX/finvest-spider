# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy import Request
from ..items import FinvestItem


class A36krSpider(scrapy.Spider):
    name = '36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['https://36kr.com/api/newsflash?column_ids=69&no_bid=true&b_id=&per_page=300']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_request(self):
        yield Request(self.start_urls, headers=self.headers)

    def parse(self, response):
        item = FinvestItem()
        # 转化为 unicode 编码的数据
        sites = json.loads(response.body_as_unicode())

        src_pattern = re.compile('。（(.*)）')

        for i in sites['data']['items']:
            item['link'] = i['news_url']
            item['title'] = i['title']
            if src_pattern.search(i['description']) == None:
                item['source'] = "36Kr"
            else:
                item['source'] = src_pattern.search(i['description']).group(1)
            item['create_time'] = i['published_at']
            item['content'] = i['description']
            
            yield item
