# -*- coding: utf-8 -*-
import scrapy


class FinvestItem(scrapy.Item):
    # Common Information

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

    # Funding Round
    funding_round = scrapy.Field()

    # Abstract
    abstract = scrapy.Field()
