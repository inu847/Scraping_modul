from scrapy import Spider
from scrapy.http import Request, FormRequest


class EplanSpider(Spider):
    name = 'eplan'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()

        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(url, callback=self.parse_application)
    
    def parse_application(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()

        yield Request(response.urljoin(app_url), callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '42'},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self, response):
        application_url = response.xpath('//td/a/@href').extract()

        for url in application_url:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_item)
        
        next_pages = response.xpath('//li[@class="PagedList-skipToNext"]/a/@href').extract_first()
        absolute_next_pages = response.urljoin(next_pages)
        yield Request(absolute_next_pages, callback=self.parse_pages)

    def parse_item(self, response):
        btn = response.xpath('//div/input[@value="Agents"]/@style').extract_first()
        if 'display: inline;  visibility: visible;' in btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first().strip()

            address_first = response.xpath('//tr[th="Address :"]/td/text()').extract()
            address_second = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]
            address = address_first + address_second

            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td/a/text()').extract_first()
            url = response.url

            yield{'name': name,
                  'address': address,
                  'phone': phone,
                  'fax': fax,
                  'email': email,
                  'url': url}
        else:
            self.logger.info('Button not found in page')
        # absolute_btn_click = response.joinurl(btn)
        # yield Request(absolute_btn_click, callback=self.pages)

            