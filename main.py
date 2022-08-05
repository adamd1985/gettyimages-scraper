from gettyscraper.spiders.gettyscraper import GettyImagesSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

import os

# The path seen from root, ie. from main.py
settings_file_path = 'gettyscraper.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)
for topic in ["restaurant", "hotel", "swimming%20pool"]:
    runner.crawl(GettyImagesSpider, topic)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()
