import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest


class AliexSpider(scrapy.Spider):
    name = 'aliex'
    allowed_domains = ['aliexpress.com']
    start_urls = ['http://aliexpress.com/']

    def start_request(self, response):
        filter_script = """function main(splash)
                                assert(splash:go(splash.args.url))
                                splash:wait(5)

                                local get_element_dim_by_xpath = splash:jsfunc([[
                                    function(xpath) {
                                        var element = document.evaluate(xpath, document, null,
                                            XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                        var element_rect = element.getClientRects()[0];
                                        return {"x": element_rect.left, "y": element_rect.top}
                                    }
                                ]])
                        end"""
