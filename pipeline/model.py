import mysql.connector
from datetime import datetime
import json
from peewee import *
import datetime

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

class CrawlData(BaseModel):
    class Meta:
        table_name = 'crawl_data'
    domain = TextField()
    title = TextField()
    url = TextField()
    content = TextField()
    date = DateTimeField(default=None)
    created_at = DateTimeField(default=datetime.datetime.now)

class Category(BaseModel):
    class Meta:
        table_name = 'categories'
    name = TextField()
    domain = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

class CategoryCrawl(BaseModel):
    class Meta:
        table_name = 'category_crawl'
    name = TextField()
    category = ForeignKeyField(Category, backref='category')
    items = ForeignKeyField(CrawlData, backref='items')
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)

mydb.connect()

mydb.create_tables([CrawlData, Category, CategoryCrawl])

mydb.close()