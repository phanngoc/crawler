import mysql.connector
from datetime import datetime
import json
from peewee import *
import peewee as pw

from regex import F

mydb = MySQLDatabase(
        "pyml",
        host="127.0.0.1", 
        port=13306,
        user="root",
        passwd="root",
        charset='utf8'  # Specify the character set as UTF-8
        )

class BaseModel(Model):
    class Meta:
        database = mydb

class JSONField(pw.TextField):
    """
    Class to "fake" a JSON field with a text field. Not efficient but works nicely
    """
    def db_value(self, value):
        """Convert the python value for storage in the database."""
        return value if value is None else json.dumps(value)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        return value if value is None else json.loads(value)

class CrawlData(BaseModel):
    class Meta:
        table_name = 'crawl_data'
    domain = TextField(null=True)
    title = TextField(null=True)
    url = TextField(null=True)
    content = TextField(default=None, null=True)
    date = DateTimeField(default=None, null=True)
    data = JSONField(null=True)
    created_at = DateTimeField(default=datetime.now)


mydb.connect()
mydb.create_tables([CrawlData])
mydb.close()

def create_article(item, is_update=False):
    query = CrawlData.select().where(CrawlData.url == item['url'])

    if len(query) > 0:
        itemDB = query[0]
        if is_update:
            if 'title' in item:
                itemDB.title = item['title']
            if 'content' in item:
                itemDB.content = item['content']
            if 'date' in item:
                itemDB.date = item['date']
            if 'data' in item:
                itemDB.data = item['data']

            itemDB.save()
            return itemDB
        else:
            return False

    data = {
        'domain': item['domain'],
        'title': item['title'],
        'content': item['content'],
        'url': item['url'],
        'date': item['date'] if 'date' in item else None,
        'created_at': datetime.now(),
        'data': item['data'] if 'data' in item else None,
    }

    return CrawlData.create(**data)
