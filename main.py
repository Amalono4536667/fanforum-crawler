
from scrapy.crawler import CrawlerProcess

from fanforum_crawler.spiders.fanforum_spider import FanForumSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(FanForumSpider)
    process.start()
