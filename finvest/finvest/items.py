# -*- coding: utf-8 -*-

# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FinvestItem(scrapy.Item):
    # Common Infomation

    # Article Title
    title = scrapy.Field()

    # Article Create Time
    create_time = scrapy.Field()

    # Article Detail Link
    link = scrapy.Field()

    # Article Content
    content = scrapy.Field()

    # Article Source
    source = scrapy.Field()
