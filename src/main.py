from scrapy.crawler import CrawlerProcess

from spiders import FanForumSpider

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(FanForumSpider)
    process.start()
