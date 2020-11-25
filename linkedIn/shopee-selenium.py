from time import sleep
from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
sleep(0.5)

driver.get('https://shopee.co.id/')
sleep(5)

driver.find_element_by_xpath('//*[@class="shopee-popup__close-btn"]').click()
sleep(3)

driver.find_element_by_xpath('//a[text()="Login"]').click()
sleep(5)

username_input = driver.find_element_by_name('loginKey')
username_input.send_keys('rahayukh_collect')
sleep(0.5)

password_input = driver.find_element_by_name('password')
password_input.send_keys('Semogaberkah')
sleep(0.5)

driver.find_element_by_xpath('//button[text()="Log in"]').click()
sleep(5)

driver.find_element_by_xpath('//*[@class="shopee-popup__close-btn"]').click()
sleep(3)

driver.get('https://seller.shopee.co.id/webchat/conversations')
sleep(5)