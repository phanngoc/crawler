import mysql.connector
from datetime import datetime
import json
from peewee import *
import peewee as pw

from regex import F

mydb = PostgresqlDatabase(
        "news_data",
        host="127.0.0.1", 
        port=5432,
        user="postgres",
        password="password",
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

def create_article(item):
    query = CrawlData.select().where(CrawlData.url == item['url'])

    if len(query) > 0:
        itemDB = query[0]
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



import csv

class CSVWriter:
    def __init__(self, csv_file_path, fieldnames):
        self.csv_file_path = csv_file_path
        self.fieldnames = fieldnames

        # Write headers if the file doesn't exist
        file_exists = False
        try:
            with open(csv_file_path, mode='x'):
                pass
        except FileExistsError:
            file_exists = True

        if not file_exists:
            with open(csv_file_path, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

    def push_item(self, data_dict):
        with open(self.csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writerow(data_dict)

    def truncate_file(self):
        try:
            with open(self.csv_file_path, mode='w', newline='') as csv_file:
                csv_file.write('')
            print(f"CSV file '{self.csv_file_path}' has been truncated.")
        except Exception as e:
            print(f"Error truncating CSV file '{self.csv_file_path}': {e}")