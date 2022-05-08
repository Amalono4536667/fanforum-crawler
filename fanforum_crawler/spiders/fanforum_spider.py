from scrapy import Request, Spider
from scrapy.loader import ItemLoader

from fanforum_crawler.items import CommentItem


class FanForumSpider(Spider):
    allowed_domains = ['sodika.org']
    name = "fanforumspider"

    def start_requests(self):
        yield Request('https://forum.sodika.org', callback=self.parse)

    def parse(self, response, **kwargs):
        comments = response.xpath('//div[contains(@class, "comment")]')
        for comment in comments:
            loader = ItemLoader(item=CommentItem(), selector=comment)
            loader.add_xpath('author', './div[@class="header"]//strong[contains(@class,"verified")]/text()')
            loader.add_xpath('created_at', './div[@class="header"]//span[@class="date"]/text()')
            loader.add_xpath('votes', './div[@class="header"]//b[starts-with(@class,"votes-")]/text()')
            loader.add_xpath('quote', './div[@class="content"]//div[@class="quote"]/text()')
            loader.add_xpath('content', './div[@class="content"]//div[@class="innerDiv"]/text()')
            loader.add_xpath('title', './div[@class="header"]//span/@title')
            loader.add_xpath('signature', './div[@class="content"]//i[@class="signature"]/text()')
            yield loader.load_item()
