
from scrapy.crawler import CrawlerProcess

from spiders.fanforum_spider import FanForumSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(FanForumSpider)
    process.start()
