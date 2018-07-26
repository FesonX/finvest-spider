# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
import time

from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter

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
        self.coll = self.db['finvest']

        if (self.coll.find_one({"title": item['title']}) == None): 
            content = item['content']
            title = item['title']

            # get funding round
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

        else:
            raise DropItem("Duplicate data %s" % item)


class SaveToCsvPipeline(object):
    """
    use for export items to csv
    file will be saved as datetime.csv (Y-M-D H-M-S) in the directory 'data'
    """

    def __init__(self):
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        filename = 'data/' + now + ".csv"
        self.file = open(filename, 'wb' )
        self.export = CsvItemExporter(self . file)
        self.export.fields_to_export = ['title','create_time','link','content',
        'source','funding_round']
    
    def spider_opened(self, spider):
        # now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        # if (spider.name == "trjcn"):
        #     # 路径 + 时间.csv
        #     filename = 'data/trjcn ' + now + ".csv"
        # if (spider.name == "cvnews"):
        #     # 路径 + 时间.csv
        #     filename = 'data/cvnews ' + now + ".csv"
        # else:
        #     filename = 'data/36kr ' + now + ".csv"
        
        # self.file = open(filename, 'wb' )
        # self.export = CsvItemExporter(self . file)
        # self.export.fields_to_export = ['title','create_time','link','content',
        # 'source','funding_round']
        self.export.start_exporting

    def spider_closed(self, spider):
        self.export.finish_exporting
        self.file.close()

    def process_item(self, item, spider):
        self.export.export_item(item) 
        return item