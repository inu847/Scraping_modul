import scrapy


class WebchatSpider(scrapy.Spider):
    name = 'webchat'
    allowed_domains = ['mall.shopee.co.id']
    start_urls = ['http://mall.shopee.co.id/']

    def parse(self, response):
        
