from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from urllib.parse import urlparse
from urllib.parse import parse_qs
import re


class GettyImagesSpider(CrawlSpider):
    """Simple spider that extracts URLs of getty images.

    Start_urls can be overridden in the constructor for dynamic generation.
    """
    name = "gettyimages"
    allowed_domains = ["gettyimages.com"]
    start_urls = []
    rules = [
        Rule(
            LinkExtractor(
                deny=(),
                allow=r"/image.*", unique=True),
            callback="parse",
            errback="errback",
            follow=False,
        )
    ]

    def __init__(self, topic, *args, **kwargs):
        """Constructor"""
        super(GettyImagesSpider, self).__init__(*args, **kwargs)
        self.start_urls.append('https://www.gettyimages.com/search/2/image?phrase={topic}&page=1')

    def parse(self, response):
        """Image processor"""
        self.logger.debug(f'Processing: {response.request.url}')
        xpath_sel = response.xpath(
            "//picture"
        ).xpath(
            "img/@src"
        )

        for img in xpath_sel:
            urls = img.getall()
            if urls is not None and len(urls) != 0:
                for url in urls:
                    yield {'url': url}

        parsed_url = urlparse(response.request.url)
        captured_value = parse_qs(parsed_url.query)
        page = 1 if captured_value is None or 'page' not in captured_value else int(
            captured_value['page'][0]) + 1
        abs_url = re.sub('page=\d', f'page={page}', response.request.url)

        max_pages = xpath_sel = response.xpath(
            "//span[@class =  'PaginationRow-module__lastPage___k9Pq7']/text()"
        ).get()

        if max_pages is not None and len(max_pages) > 0 and int(max_pages) >= page:
            yield Request(
                url=abs_url,
                callback=self.parse
            )

    def errback(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)
