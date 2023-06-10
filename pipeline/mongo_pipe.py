from pymongo import MongoClient
import pymongo
from datetime import datetime
import json

class MongoWriterPipeline(object):
    def open_spider(self, spider):
        CONNECTION_STRING = "mongodb://root:123456@localhost/admin"
        self.db = MongoClient(CONNECTION_STRING)

    def close_spider(self, spider):
        print('close spider')
        self.db.close()

    def process_item(self, item, spider):
        print(item);
        item['created_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'tags' in item:
            tagsstr = json.dumps(item['tags'])
            item['tags'] = tagsstr

        self.db.admin.article.insert_one(item)
        return item