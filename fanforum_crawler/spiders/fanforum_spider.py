from scrapy import Request, Spider
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from fanforum_crawler.items import CommentItem


class FanForumSpider(Spider):
    NUMBER_OF_PAGES_TO_CRAWL = 50

    allowed_domains = ['sodika.org']
    name = 'fanforumspider'

    def generate_urls(self, response):
        end = int(response.xpath('//div[@class="paginator"]//a/text()')[-1].extract())
        yield self.parse(response)

        start = 0 if end < self.NUMBER_OF_PAGES_TO_CRAWL else end - self.NUMBER_OF_PAGES_TO_CRAWL
        for i in range(start, end):
            yield Request(f'https://forum.sodika.org/index.php?pageNo={i}', callback=self.parse)

    def start_requests(self):
        return [Request('https://forum.sodika.org', callback=self.generate_urls)]

    def parse(self, response: HtmlResponse, **kwargs):
        for comment in response.xpath('//div[contains(@class, "comment")]'):
            loader = ItemLoader(item=CommentItem(), selector=comment)
            loader.add_xpath('author', './div[@class="header"]//strong[contains(@class,"verified")]/text()')
            loader.add_xpath('created_at', './div[@class="header"]//span[@class="date"]/text()')
            loader.add_xpath('votes', './div[@class="header"]//b[starts-with(@class,"votes-")]/text()')
            loader.add_xpath('quote', './div[@class="content"]//div[@class="quote"]/text()')
            loader.add_xpath('content', './div[@class="content"]//div[@class="innerDiv"]/text()')
            loader.add_xpath('title', './div[@class="header"]//span/@title')
            loader.add_xpath('signature', './div[@class="content"]//i[@class="signature"]/text()')
            yield loader.load_item()
