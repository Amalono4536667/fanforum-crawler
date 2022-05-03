from pickle import GET
from requests import Response
from scrapy import Request, Spider


class FanForumSpider(Spider):
    allowed_domains = ['sodika.org']
    autothrottle_enabled=True
    name = 'FanForum'

    def start_requests(self):
        yield Request('https://forum.sodika.org', callback=self.parse)

    def parse(self, response: Response):
        pass
