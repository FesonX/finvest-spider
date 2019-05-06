# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import re
import time
import pymysql

from scrapy import log
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import CloseSpider
from middleware.textSummary import TextSummary


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

        # if self.coll.find_one({"title": item['title']} is None):
        if 1 is 1:
            content = item['content']
            title = item['title']

            # get funding round
            # U can test here: http://tool.oschina.net/regex
            fin = re.compile(r'(?:p|P)re-?(?:A|B)轮|(?:A|B|C|D|E)(?:\+)?1?2?3?轮|(?:天使|种子|首)轮|IPO|(?:p|P)re-?IPO')
            result = fin.findall(title)
            if len(result) == 0:
                result = "未透露"
            else:
                result = ''.join(result)

            content = content.replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
            content = content.replace('\n', '').strip()
            # delete html label in content
            rule = re.compile(r'<[^>]+>', re.S)
            content = rule.sub('', content)

            item['content'] = content
            item['funding_round'] = result
            # self.coll.insert(dict(item))
            return item

        else:
            raise DropItem("Duplicate data %s" % item)


class SaveToMysqlPipeline(object):
    """
    for saving to mysql
    """
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            pattern = re.compile(r'(?:com|cn)')
            pos = pattern.search(item['link']).end()
            website = item['link'][:pos]

            self.cursor.execute("""select create_time from news where link like '%s%%' limit 1""" % website)
            res = self.cursor.fetchone()
            if res[2] >= item['create_time']:
                raise CloseSpider("Duplicate Data")

            self.cursor.execute("""select * from news where title = %s and link = %s""", (str(item['title']), str(item['link'])))
            res = self.cursor.fetchone()
            if res:
                raise DropItem("Duplicate item found: %s" % item['title'])
            else:
                content = item['content']
                title = str(item['title'])

                textSummary = TextSummary()
                textSummary.set_text(title, content)
                abstract = textSummary.calc_summary()

                # get funding round
                # U can test here: http://tool.oschina.net/regex
                fin = re.compile(r'(?:p|P)re-?(?:A|B)轮|(?:A|B|C|D|E)(?:\+)?1?2?3?轮|(?:天使|种子|首)轮|IPO|(?:p|P)re-?IPO')
                result = fin.findall(title)
                if len(result) == 0:
                    result = "未透露"
                else:
                    result = ''.join(result)

                content = content.replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
                content = content.replace('\n', '').strip()
                # delete html label in content
                rule = re.compile(r'<[^>]+>', re.S)
                content = rule.sub('', content)

                item['content'] = content
                item['funding_round'] = result
                self.cursor.execute(
                    'insert into news(title, create_time, link, content, source, abstract, funding_round) value (%s,%s,%s,%s,%s,%s,%s)'
                    , (title, str(item['create_time']), str(item['link']), content, item['source']), abstract, result
                )
                self.connect.commit()

        except Exception as e:
            print(e)
        return item


class SaveToCsvPipeline(object):
    """
    use for export items to csv
    file will be saved as datetime.csv (Y-M-D H-M-S) in the directory 'data'
    """

    def __init__(self):
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        filename = 'data/' + now + ".csv"
        self.file = open(filename, 'wb')
        self.export = CsvItemExporter(self.file)
    
    def spider_opened(self):
        pass

    def spider_closed(self):
        self.file.close()

    def process_item(self, item, spider):

        content = item['content']
        title = str(item['title'])

        textSummary = TextSummary()
        textSummary.set_text(title, content)
        abstract = textSummary.calc_summary()
        item['abstract'] = abstract

        fin = re.compile(r'(?:p|P)re-?(?:A|B)轮|(?:A|B|C|D|E)(?:\+)?1?2?3?轮|(?:天使|种子|首)轮|IPO|(?:p|P)re-?IPO')
        result = fin.findall(title)
        if len(result) == 0:
            result = "未透露"
        else:
            result = ''.join(result)
        item['funding_round'] = result
        content = content.replace(u'<p>', u' ').replace(u'</p>', u' ').replace(u'\n\t', ' ').strip()
        content = content.replace('\n', '').strip()
        item['content'] = content
        self.export.export_item(item)
        self.export.fields_to_export = ['title', 'create_time', 'link', 'content', 'source', 'funding_round',
                                        'abstract']
        return item
