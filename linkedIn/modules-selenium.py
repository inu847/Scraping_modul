from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector

driver = webdriver.Chrome()
driver.maximize_window()
sleep(0.5)

# driver.get('https://shopee.co.id/')
# sleep(5)

# driver.find_element_by_xpath('//*[@class="shopee-popup__close-btn"]').click()
# sleep(3)

# driver.find_element_by_xpath('//a[text()="Login"]').click()
# sleep(5)

# username_input = driver.find_element_by_name('loginKey')
# username_input.send_keys('rahayukh_collect')
# sleep(0.5)

# password_input = driver.find_element_by_name('password')
# password_input.send_keys('Semogaberkah')
# sleep(0.5)

# driver.find_element_by_xpath('//button[text()="Log in"]').click()
# sleep(5)

# driver.find_element_by_xpath('//*[@class="shopee-popup__close-btn"]').click()
# sleep(3)

driver.get('https://seller.shopee.co.id/webchat/conversations')
sleep(5)

username = driver.find_element_by_xpath('//input[@type="text"]')
username.send_keys('adin72978@gmail.com')
sleep(0.5)

password = driver.find_element_by_xpath('//input[@type="password"]')
password.send_keys('Komputer007')
sleep(0.5)

password.send_keys(Keys.RETURN)
sleep(5)

btn_chat = driver.find_elements_by_xpath('//*[@class="_1T5PCuIeve"]')
# btn_chat = [btn.get_attribute for btn in btn_chat]
for btn in btn_chat:
    btn.click()
    sleep(3)

# sel = Selector(driver.page_source)

# name = sel.xpath('//*[@class="_2YvuyWzYMq"]/text()').extract()
# chat = sel.xpath('//*[@class="_2VgQumDqQ2"]/span/text()').extract()
# date_chat = sel.xpath('//*[@class="_3Ye0QdUU1-"]/text()').extract()