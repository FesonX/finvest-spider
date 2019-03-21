# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from fake_useragent import UserAgent


class RandomUserAgent(UserAgentMiddleware):
    def process_request(self, request, spider):
        ua = UserAgent(verify_ssl=False)
        request.headers.setdefault('User-Agent', ua.random)
