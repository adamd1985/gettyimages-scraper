from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError


class GettyImagesSpider(CrawlSpider):
    """Simple spider that extracts URLs of getty images.

    Start_urls can be overridden in the constructor for dynamic generation.
    """
    name = "gettyimages"
    allowed_domains = ["gettyimages.com"]
    start_urls = [
        "https://www.gettyimages.com/search/2/image?phrase=restaurant",
        "https://www.gettyimages.com/search/2/image?phrase=hotel",
        "https://www.gettyimages.com/search/2/image?phrase=swimming%20pool"
    ]

    rules = [
        Rule(
            LinkExtractor(
                deny=(),
                allow=r"/image.*", unique=True),
            callback="parse",
            errback="errback",
            follow=False,
        ),
        Rule(
            LinkExtractor(
                deny=(),
                allow=(r"/.+page=\d+"), unique=True),
            errback="errback",
            follow=True,
        ),
    ]

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(GettyImagesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        """Image processor"""
        self.logger.info(f'Processing: {response}')
        url = response.xpath(
            "//picture[contains('img')]//parent::picture/attr('url')"
        )
        img_data = {
            "url": url,
        }

        yield img_data

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
