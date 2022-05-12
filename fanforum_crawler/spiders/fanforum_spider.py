import pendulum
from scrapy import Request, Spider
from scrapy.http import HtmlResponse

from fanforum_crawler.items import Comment, Quote
from fanforum_crawler import string_utils


class FanForumSpider(Spider):
    NUMBER_OF_PAGES_TO_CRAWL = 1
    XPATH_TEXT = './text()'

    allowed_domains = ['sodika.org']
    name = 'fanforumspider'

    def _generate_urls(self, response: HtmlResponse):
        end = int(response.xpath('//div[@class="paginator"]//a/text()')[-1].extract())
        yield self.parse(response)

        start = 0 if end < self.NUMBER_OF_PAGES_TO_CRAWL else end - self.NUMBER_OF_PAGES_TO_CRAWL
        for i in range(start, end):
            yield Request(f'https://forum.sodika.org/index.php?pageNo={i}', callback=self.parse)

    def start_requests(self) -> list[Request]:
        return [Request('https://forum.sodika.org', callback=self._generate_urls)]

    def parse(self, response: HtmlResponse, **kwargs):
        for comment in response.xpath('//div[contains(@class, "comment")]'):
            content_selector = comment.xpath('./div[@class="content"]//div[@class="innerDiv"]')
            content = string_utils.join(content_selector.xpath(self.XPATH_TEXT).extract()) if content_selector else None
            quote_selector = comment.xpath('./div[@class="content"]//div[@class="quote"]')
            quote = Quote(author=quote_selector.xpath('./div[@class="author"]/text()').extract()[0],
                          content=string_utils.join(
                              quote_selector.xpath(self.XPATH_TEXT).extract())) if quote_selector else None
            signature_selector = comment.xpath('./div[@class="content"]//i[@class="signature"]')
            signature = string_utils.join(
                signature_selector.xpath(self.XPATH_TEXT).extract()) if signature_selector else None

            yield Comment(
                author=comment.xpath('./div[@class="header"]//strong/text()').get(),
                created_at=pendulum.from_format(
                    comment.xpath('./div[@class="header"]//span[@class="date"]/text()').get(), 'MMM DD, YYYY HH:mm:ss',
                    tz='Europe/Budapest'),
                votes=int(comment.xpath('./div[@class="header"]//b[starts-with(@class,"votes-")]/text()').get()),
                quote=quote,
                content=content,
                title=comment.xpath('./div[@class="header"]//span/@title').get(),
                signature=signature
            ).dict()
