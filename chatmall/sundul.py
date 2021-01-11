from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
from parsel import Selector

chrome_options = Options()
chrome_options = chrome_options.add_argument("--headless")
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://seller.shopee.co.id/portal/product/list/all?page=1&order=sales_dsc')
driver.implicitly_wait(30)

user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
user.send_keys('oktawasxmarket')
driver.implicitly_wait(20)

passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
passwd.send_keys('semogaberkah')
driver.implicitly_wait(20)
    
driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()

driver.find_element_by_xpath('//*[@class="guide-back"]').click()
driver.implicitly_wait(10)

driver.find_elements_by_xpath('//*[@class="view-modes"]/div')[0].click()
driver.implicitly_wait(10)

# driver.find_element_by_xpath('//*[@class="EntryLayout_portal__2oe7T"]/button').click()
# driver.implicitly_wait(10)

# dsc = driver.find_element_by_xpath('//*[@class="shopee-order-dsc order-icon shopee-icon"]')[2].click()
# driver.implicitly_wait(10)

driver.find_elements_by_xpath('//*[@class="product-list-card product-list-item"]')
driver.implicitly_wait(10)

sel = Selector(text=driver.page_source)
boost = driver.find_element_by_xpath('//*[@class="shopee-popper dropdown-menu"]')
views = sel.xpath('//*[@class="product-list-item__td product-variation__sales"]/div/text()').extract()
for view in views:
    view.strip()
    print(view)
    if view != '0':
        boost.click()
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[@class="shopee-popper dropdown-menu"]/ul/li[5]').click()
        print("sundul success")
    else:
        continue


# driver.implicitly_wait(10)
# for (view, vi) in zip (views, vie):
#     print(view)
#     if view == '0':
#         print('Tidak ada view > 0')
#     else:
#         vi.click()
#         sleep(2)
#         sel.xpath('//*[@class="shopee-dropdown-menu"]')
#         driver.find_element_by_xpath('//*[@class="shopee-dropdown-menu"]/li[4]')
#         driver.find_elements_by_xpath('//*[@class="product-actions-button product-mul-actions-button"]')[0].click()
#         driver.find_elements_by_xpath('//*[@class="boost-button"]')

# driver.implicitly_wait(5)

# btn_more = driver.find_elements_by_xpath('//*[@class="dropdown shopee-dropdown"]')
# for btn in btn_more:
#     btn.click()
#     driver.implicitly_wait(10)
#     sel = Selector(text=driver.page_source)
#     up = sel.xpath('//*[@class="boost-button-text"]/text()').extract_first().strip()
#     if up == 'Naikkan Produk':
#         driver.find_element_by_xpath('//*[@class="boost-button-text"]').click()
#         driver.implicitly_wait(10)
#         btn.click()
#     else:
#         btn.click()
#         continue
        
#     sel.xpath('//*[@class="shopee-dropdown-menu"]')

        
# view.find_element_by_xpath('//*[@class="shopee-popper"]').click()
# driver.implicitly_wait(30)
# view.find_element_by_xpath('//*[@class="shopee-dropdown-item"]').click()
# driver.implicitly_wait(30)
# view.find_element_by_xpath('//*[@class="boost-button-text"]').click()

