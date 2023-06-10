from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

from crawl import GenkSpider, VnExpressSpider, Kenh14Spider, DantriSpider, DevToApi, ThanhnienSpider, VneconomySpider

process.crawl(VneconomySpider)
# process.crawl(GenkSpider)
# process.crawl(Kenh14Spider)
# process.crawl(DantriSpider)
# process.crawl(ThanhnienSpider)


# process.crawl(DevToApi)

process.start()