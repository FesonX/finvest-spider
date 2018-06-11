# -*- coding: utf-8 -*-
import scrapy
from ..items import FinvestItem
from scrapy.linkextractors import LinkExtractor


class TrjcnSpider(scrapy.Spider):
    name = 'trjcn'
    # allowed_domains = ['news.trjcn.com/']
    start_urls = ['http://news.trjcn.com/list_70.html']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def parse(self, response):
        #
        le = LinkExtractor(restrict_css='div.newMain>div>ul>li>h2')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.news_parse, headers=self.headers)
        #
        le = LinkExtractor(restrict_css='div.newMain>div>div>a:nth-child(7)')
        links = le.extract_links(response)
        if links:
            next_url = links[-1].url
            yield scrapy.Request(next_url, callback=self.parse, headers=self.headers)
            
    def news_parse(self, response):
        item = FinvestItem()
        item['title'] = response.xpath('//div[@class="newDetail"]/h2/text()').extract_first()
        item['create_time'] = response.xpath('//div[@class="fl"]/span[1]/text()').extract_first()
        item['link'] = response.url
        item['content'] = response.xpath('string(//div[@id="newDetailCont"])').extract_first().replace(u'\n\n\n\t', u'\n').strip()
        item['source'] = response.xpath('//div[@class="fl"]/span[2]/text()').extract_first()[3:]
        
        yield item
