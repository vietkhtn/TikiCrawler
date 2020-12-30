# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.core.downloader.handlers import file
from scrapy.exporters import CsvItemExporter


class TikicrawlerPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        self.db = self.conn['TikiCrawler']

    def spider_opened(self, spider):
        self.exporter = CsvItemExporter(file, encoding='cp1252')

    def process_item(self, item, spider):
        self.collection = self.db[type(item).__name__]
        self.collection.insert(dict(item))
        return item
