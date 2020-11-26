from scrapy import Spider
from selenium import webdriver


class AliexSpider(Spider):
    name = 'aliex'
    allowed_domains = ['aliexpress.com']

    def start_request(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get('https://www.aliexpress.com/')
        
        

