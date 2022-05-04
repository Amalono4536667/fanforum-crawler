from pickle import GET
from requests import Response
from scrapy import Request, Spider
from scrapy.loader import ItemLoader

from fanforum_crawler.items import CommentItem


class FanForumSpider(Spider):
    allowed_domains = ['sodika.org']
    autothrottle_enabled = True
    name = 'fanforumspider'

    def start_requests(self):
        yield Request('https://forum.sodika.org', callback=self.parse)

    def parse(self, response: Response):
        comments = response.xpath('//div[@class="comment"]')
        for comment in comments:
            loader = ItemLoader(item=CommentItem(), selector=comment)
            loader.add_xpath('author', '//span[@class="authorText"]')
            loader.add_xpath('created_at', '//span[@class="date"]')
            loader.add_xpath('votes', '//b[starts-with(@class,"votes-")]')
            loader.add_xpath('quote', '//div[@class="quote"]')
            loader.add_xpath('content', '//div[@class="innerDiv"]')
            yield loader.load_item()
