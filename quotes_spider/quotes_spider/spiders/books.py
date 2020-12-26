# from scrapy.spiders import CrawlSpider, Rule
import os
import csv
import glob
import pymysql
from scrapy import Spider
# from selenium import webdriver
# from scrapy.selector import Selector
from scrapy.http import Request
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException
# from quotes_spider.items import BooksCrawlerItem
# from scrapy.linkextractors import LinkExtractor

def product_info(response, value):
    return response.xpath('//th[text()="' +value+ '"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)
    
        # process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com/')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # product information data points
        upc = product_info(response, 'UPC')
        product_type =  product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl. tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')

        yield {
            'title': title,
            'price': price,
            'image_url': image_url,
            'rating': rating,
            'description': description,
            'upc': upc,
            'product_type': product_type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews
        }
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        
        mydb = pymysql.connect(host='127.0.0.1',
                               user='root',
                               database='webchat')

        cursor = mydb.cursor()

        csv_data = csv.reader(open(csv_file))

        row_count = 0
        for row in csv_data:
            if row_count != 0:
                cursor.execute('INSERT IGNORE INTO books_db(title, rating, upc, product_type) VALUES(%s, %s, %s, %s)', row)
            row_count += 1

        mydb.commit()
        cursor.close()

    # (LinkExtractor(allow=('music')) untuk mendapatkan kategori music
    # rules = (Rule(LinkExtractor(), callback='parse_page', follow=False),)

    # def parse_page(self, response):
    #     yield('URL': response.url)

    # def start_requests(self):
    #     self.driver = webdriver.Chrome()
    #     self.driver.get('http://books.toscrape.com')

    #     sel = Selector(text=self.driver.page_source)
    #     books = sel.xpath('//h3/a/@href').extract()
    #     for book in books:
    #         url = 'http://books.toscrape.com/' + book
    #         yield Request(url, callback=self.parse_book)

    #     while True:
    #         try:

    #             next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
    #             sleep(3)
    #             self.logger.info('Sleeping for 3 Second')
    #             next_page.click()

    #             sel = Selector(text=self.driver.page_source)
    #             books = sel.xpath('//h3/a/@href').extract()
    #             for book in books:
    #                 url = 'http://books.toscrape.com/catalogue' + book
    #                 yield Request(url, callback=self.parse_book)

    #         except NoSuchElementException:
    #             self.logger.info('No more pages to load')
    #             self.driver.quit()
    #             break

    # def parse_book(self, response):
    #     title = response.css('h1::text').extract_first()
    #     url = response.request.url
    #     yield {'title': title, 'url':url}

        # items = BooksCrawlerItem()
        # title = response.css('h1::text').extract_first()
        # url = response.request.url
    
        # items['title'] = title
        # items['url'] = url
        # yield items
