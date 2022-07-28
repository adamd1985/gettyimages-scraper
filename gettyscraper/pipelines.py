import sqlite3
from itemadapter import ItemAdapter


class SpiderPipeline(object):
    def open_spider(self, spider):
        # called when the spider is opened
        self.con = sqlite3.connect('urls.db')  # create a DB
        self.cur = self.con.cursor()
        self.cur.execute(
            '''DROP TABLE IF EXISTS urls''')  # drop table if already exists
        self.cur.execute('''CREATE TABLE urls (url)''')  # create a table
        self.con.commit()

    def close_spider(self, spider):
        # called when the spider is closed
        self.con.close()

    def process_item(self, item, spider):
        # called for each item crawled from spiders/quotes-spiders.py
        # insert the each item crawled into DB
        self.cur.execute(
            "INSERT INTO urls (url) VALUES( '" + item['url'] + "')")
        self.con.commit()
        return item
