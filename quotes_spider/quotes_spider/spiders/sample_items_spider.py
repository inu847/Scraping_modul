# -*- coding: utf-8 -*-
import os
import csv
import glob
import scrapy
from openpyxl import Workbook
# from scrapy_items_example.items import ScrapyItemsExampleItem


class SampleItemsSpiderSpider(scrapy.Spider):
    name = "sample_items_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = (
        'http://quotes.toscrape.com/',
    )

    def parse(self, response):
        authors = response.xpath('//*[@itemprop="author"]/text()').extract()
        yield {'authors': authors}

    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r') as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')

        # item = ScrapyItemsExampleItem()
        # item['authors'] = authors
        # return item
