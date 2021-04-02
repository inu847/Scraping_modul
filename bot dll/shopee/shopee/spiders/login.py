import scrapy
from scrapy import Spider
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class LoginSpider(scrapy.Spider):
    name = 'login'
    #allowed_domains = ['seller.shopee.com']
    start_urls = ['https://seller.shopee.co.id/account/signin?next=%2Fwebchat']

    def parse(self, response):
        #token = response.xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]/text()').extract_first()
        #print(token)
        yield FormRequest(url=self.start_urls[0],
                            formdata={'username': 'mukhtarqistore',
                                    'password_hash': 'a5b4fec9e77996b2c6f05aedac7f32a34bf941407482fcb83c4150a47e6d1f30',
                                    'remember': 'false'},
                            callback=self.parse_after_login
                        )
        

    def parse_after_login(self, response):
        open_in_browser(response)
                    
