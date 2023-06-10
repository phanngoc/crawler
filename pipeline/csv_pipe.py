import csv

class CSVWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('input-articles.csv', 'w')
        csv_columns = ['title', 'url', 'content']
        self.writer = csv.DictWriter(self.file, fieldnames=csv_columns)
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        print(item, type(item))
        self.writer.writerow(item)
        return item