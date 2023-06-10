from gettext import gettext
import logging
import queue
import scrapy
import json
import csv
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
class GenkSpider(scrapy.Spider):
    name = "genk"
    start_urls = [
        'https://genk.vn',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.kbwc-body')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        return item

    def parse(self, response):
        for quote in response.css('h4.knswli-title > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class ThanhnienSpider(scrapy.Spider):
    name = "thanhnien"
    start_urls = [
        'https://thanhnien.vn/thoi-su/',
        'https://thanhnien.vn/the-gioi/',
        'https://thanhnien.vn/tai-chinh-kinh-doanh/',
        'https://thanhnien.vn/doi-song/',
        'https://thanhnien.vn/van-hoa/',
        'https://thanhnien.vn/giai-tri/',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.content-detail-top')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        return item

    def parse(self, response):
        # print('got to parse', response.body);
        for quote in response.css('a.story__title'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class DevTo(scrapy.Spider):
    name = "genk"
    start_urls = [
        'https://dev.to/',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div#article-body')
        item['content'] = ''
        item['domain'] = self.start_urls[0]
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        return item

    def parse(self, response):
        for aElem in response.css('div.crayons-story h2.crayons-story__title > a'):
            detail_url = aElem.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': aElem.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class DevToApi(scrapy.Spider):
    name = "genk"
    domain = 'https://dev.to'
    start_urls = ['https://dev.to/search/feed_content?per_page=35&page=%d&sort_by=hotness_score&sort_direction=desc&approved=&class_name=Article' %(n) for n in range(0, 30)]

    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div#article-body')
        item['content'] = ''
        item['domain'] = self.domain
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        return item

    def parse(self, response):
        y = json.loads(response.body)
        print('parse', len(y['result']))
        for aElem in y['result']:
            detail_url = aElem['path']
            if detail_url is not None:
                item = {
                    'title': aElem['title'],
                    'url': detail_url,
                    'tags': aElem['tag_list']
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class Kenh14Spider(scrapy.Spider):
    name = "genk"
    start_urls = [
        'https://kenh14.vn',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.kbwc-body')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        return item

    def parse(self, response):
        for quote in response.css('h3.knswli-title > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class VnExpressSpider(scrapy.Spider):
    name = "vnexpress-net"
    start_urls = [
        'https://vnexpress.net/thoi-su',
        'https://vnexpress.net/the-gioi',
        'https://vnexpress.net/kinh-doanh',
        'https://vnexpress.net/khoa-hoc',
        'https://vnexpress.net/giai-tri',
        'https://vnexpress.net/the-thao',
        'https://vnexpress.net/phap-luat',
        'https://vnexpress.net/giao-duc',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('article.fck_detail')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        dateElem = soup.select_one('.header-content > .date')
        if dateElem is not None:
            item['date'] = dateElem.get_text()
            try:
                found = re.search('.*, (\d{2}/\d/\d{4}, \d{2}:\d{2}) (.*)', item['date'])
                # found = re.search('ba, \d{2}', date_time_str)
                item['date'] = datetime.strptime(found.groups()[0], '%d/%m/%Y, %H:%M')
                # print(found.groups()[0])
            except AttributeError:
                pass
        else:
            item['date'] = None
        return item

    def parse(self, response):
        for quote in response.css('h3.title-news > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class DantriSpider(scrapy.Spider):
    name = "dantri"
    start_urls = [
        'https://dantri.com.vn',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.singular-content')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        return item

    def parse(self, response):
        for quote in response.css('h3.article-title > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request


class VietStockSpider(scrapy.Spider):
    name = "dantri"
    start_urls = [
        'https://vietstock.vn/the-gioi.htm',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.singular-content')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]
        return item

    def parse(self, response):
        for quote in response.css('h3.article-title > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

class VneconomySpider(scrapy.Spider):
    name = "vneconomy"
    start_urls = [
        'https://vneconomy.vn/kinh-te-the-gioi.htm',
    ]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'ITEM_PIPELINES': {'pipeline.mysql_pipe.MysqlWriterPipeline': 1}, # Used for pipeline 1
    }

    def parse_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.body, 'html.parser')
        bodyElem = soup.select_one('div.detail__content')
        item['content'] = ''
        if bodyElem is not None:
            item['content'] = bodyElem.get_text()
        item['domain'] = self.start_urls[0]

        dateElem = soup.select_one('div.detail__meta')
        item['date'] = ''
        if dateElem is not None:
            item['date'] = dateElem.get_text()
        item['date'] = datetime.strptime(item['date'], '%H:%M %d/%m/%Y')
        print('parse_content:', item['date'])
        return item

    def parse(self, response):
        for quote in response.css('h3.story__title > a'):
            detail_url = quote.css('a::attr("href")').extract_first()
            if detail_url is not None:
                item = {
                    'title': quote.css('a::text').extract_first(),
                    'url': detail_url,
                }
                request = scrapy.Request(response.urljoin(detail_url), callback=self.parse_content)
                request.meta['item'] = item
                yield request

                