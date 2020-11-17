import scrapy
from scrapy.http import Request


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.com']
    start_urls = ['http://shopee.com/']

    def parse(self, response):
        books =  response.xpath('')
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # next product
        title = response.css('h1::text').extract_first()
        price = response.xpath('').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('.../...', 'https://shopee.co.id')

        rating = response.xpath('').extract_first()
        rating = rating.xpath('class bintang', '')

        description = response.xpath('class/id deskripsi//menggunakan following-sibling::p/text()').extract_first()

        # product informasi
        
