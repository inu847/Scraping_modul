from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome()
driver.get('https://seller.shopee.co.id/portal/product/list/all')
driver.implicitly_wait(30)

user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
user.send_keys('karmanuwmarket')
driver.implicitly_wait(20)

passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
passwd.send_keys('semogaberkah')
driver.implicitly_wait(20)
    
driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()

driver.find_element_by_xpath('//*[@class="guide-back"]').click()
driver.implicitly_wait(10)

driver.find_elements_by_xpath('//*[@class="view-modes"]/div')[0].click()
driver.implicitly_wait(5)

btn_more = driver.find_elements_by_xpath('//*[@class="dropdown shopee-dropdown"]')
for btn in btn_more:
    btn.click()
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_xpath('//*[@class="boost-button boost-no-padding"]').click()
        sleep(3)
    except:
        pass
    btn.close()
    print(btn)
        
# view.find_element_by_xpath('//*[@class="shopee-popper"]').click()
# driver.implicitly_wait(30)
# view.find_element_by_xpath('//*[@class="shopee-dropdown-item"]').click()
# driver.implicitly_wait(30)
# view.find_element_by_xpath('//*[@class="boost-button-text"]').click()

