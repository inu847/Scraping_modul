import json
from scrapy import Spider
from scrapy.http import Request


class AsosSpider(Spider):
    name = 'asos'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/men/new-in/new-in-shoes/cat/?cid=17184&nlid=mw|new+in|new+products']

    def parse(self, response):
        products = response.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
        for product in products:
            yield Request(product,
                          callback=self.parse_shoes)

        load_page = response.xpath('//a[text()="Load more"]/@href').extract_first()
        if load_page:
            yield Request(load_page,
                          callback=self.parse)

    def parse_shoes(self, response):
        product_name = response.xpath('//h1/text()').extract_first()

        product_id = response.url.split('/prd/')[1].split('?')[0]
        price_api_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds='+ product_id +'&store=ROW&currency=GBP&keyStoreDataversion=j42uv2x-26'
    
        yield Request(price_api_url,
                      meta={'product_name': product_name},
                      callback=self.parse_shoes_price)

    def parse_shoes_price(self, response):
        jsonresponse = json.loads(response.body.decode('utf-8'))
        price = jsonresponse[0]['productPrice']['current']['text']

        yield{'product_name': response.meta['product_name'],
              'price': price}