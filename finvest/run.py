# -*- coding: utf-8 -*-
import os
import time


print('The first spider opened')
os.system("scrapy crawl trjcn")
print('The second spider opened')
os.system("scrapy crawl cvnews")
print('The third spider opened')
os.system("scrapy crawl 36kr")