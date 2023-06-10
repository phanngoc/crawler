import mysql.connector
from datetime import datetime
import json
from peewee import *
from pipeline.model import CrawlData
import datetime

class MysqlWriterPipeline(object):
    def open_spider(self, spider):
        print('open spider')

    def close_spider(self, spider):
        print('close spider')

    def process_item(self, item, spider):
        data = CrawlData(
            domain = item['domain'],
            title = item['title'],
            content = item['content'],
            url = item['url'],
            date = item['date'] if 'date' in item else None
        )

        if 'tags' in item:
            tagsstr = json.dumps(item['tags'])
            data['data'] = tagsstr

        data.save()
        return item