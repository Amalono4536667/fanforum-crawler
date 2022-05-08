import pendulum
from scrapy import Request, Spider
from scrapy.http import HtmlResponse

from fanforum_crawler.items import Comment


class FanForumSpider(Spider):
    NUMBER_OF_PAGES_TO_CRAWL = 1

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
            yield Comment(
                author=comment.xpath('./div[@class="header"]//strong/text()').get(),
                created_at=pendulum.from_format(
                    comment.xpath('./div[@class="header"]//span[@class="date"]/text()').get(), 'MMM DD, YYYY HH:mm:ss',
                    tz='Europe/Budapest'),
                votes=int(comment.xpath('./div[@class="header"]//b[starts-with(@class,"votes-")]/text()').get()),
                quote=''.join(comment.xpath('./div[@class="content"]//div[@class="quote"]/text()').extract()).strip(),
                content=''.join(
                    comment.xpath('./div[@class="content"]//div[@class="innerDiv"]/text()').extract()).strip(),
                title=comment.xpath('./div[@class="header"]//span/@title').get(),
                signature=''.join(
                    comment.xpath('./div[@class="content"]//i[@class="signature"]/text()').extract()).strip()
            ).dict()
