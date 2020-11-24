from scrapy import Spider
from scrapy.http import Request


class AsosSpider(scrapy.Spider):
    name = 'asos'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/men/new-in/new-in-shoes/cat/?cid=17184&nlid=mw|new+in|new+products']

    def parse(self, response):
        products = response.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
        for product in products:
            yield Request(product,
                          callback=self.parse_shoes)

    def parse_shoes(self, response):
        product_name = response.xpath('//h1/text()').extract_first()

        product_id = response.url.split('/prd/')[1].split('?')[0]
        price_api_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds=' + product_id + '&store=ROW&currency=EUR'