# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
from scrapy.conf import settings


class FinvestPipeline(object):

    def __init__(self):
        """
        use for connecting to mongodb
        """
        # connect to db
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # ADD if NEED account and password
        # self.client.admin.authenticate(host=settings['MONGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGO_DB']]
        self.coll = self.db[settings['MONGO_COLL']]

    def process_item(self, item, spider):
        content = item['content']
        title = item['title']

        fin = re.compile(r'(?:p|P)re-?(?:A|B)轮|(?:A|B|C|D|E)+?1?2?3?轮|(?:天使轮|种子|首)轮|IPO|轮|(?:p|Pre)IPO')
        
        result = fin.findall(title)
        if(len(result) == 0):
            result = "未透露"
        else:
            result = ''.join(result)

        content = content.replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
        # delete html label in content
        rule = re.compile(r'<[^>]+>', re.S)
        content = rule.sub('', content)


        item['content'] = content
        item['funding_round'] = result
        self.coll.insert(dict(item))
        return item