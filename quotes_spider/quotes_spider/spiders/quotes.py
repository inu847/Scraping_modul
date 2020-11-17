import scrapy
from scrapy_splash import SplashRequest
# from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['http://quotes.toscrape.com/']
    start_urls = (
        'http://quotes.toscrape.com/js/',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='render.html')

    def parse(self, response):
        # h1_tag = response.xpath('//h1/a/text()').extract_first()
        # tags =  response.xpath('//*[@class="tag-item"]/a/text()').extract()
        
        # yield {'H1 tag': h1_tag, 'Tags': tags}
        # pass
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@itemprop="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@itemprop="keywords"]/@content').extract_first()

            yield{'Text' : text,
                  'Author' : author,
                  'Tags' : tags
            }
        
        script = """function main(splash)
                assert(splash:go(splash.args.url))
                splash:wait(0.3)
                button = splash:select("li[class=next] a")
                splash:set_viewport_full()
                splash:wait(0.1)
                button:mouse_click()
                splash:wait(1)
                return {url = splash:url(),
                        html = splash:html()}
            end"""

        yield SplashRequest(url=response.url,
                            callback=self.parse,
                            endpoint='execute',
                            args={'lua_source': script})

        # next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield scrapy.Request(absolute_next_page_url)