from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector

def productSundul(userName, password):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.maximize_window()
    driver.get('https://seller.shopee.co.id/portal/product/list/all?page=1&order=sales_dsc')
    driver.implicitly_wait(30)

    user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
    user.send_keys(userName)
    driver.implicitly_wait(20)

    passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
    passwd.send_keys(password)
    driver.implicitly_wait(20)

    passwd.send_keys(Keys.RETURN)
    driver.implicitly_wait(10)

    try:
        driver.find_element_by_xpath('//*[@class="guide-back"]').click()
        driver.implicitly_wait(10)
        print(userName + ' Logged In !!')
        driver.find_elements_by_xpath('//*[@class="view-modes"]/div')[0].click()
    except:
        sel = Selector(text=driver.page_source)
        error_message = sel.xpath('//*[@class="shopee-alert-title"]/text()').extract_first().strip()
        if error_message:
            print(error_message)
            writers = open('error message.txt', 'a+', encoding="utf-8")
            banned = 'Gagal Login (F02): Akun sedang ditinjau karena alasan keamanan atau karena ada aktivitas yang melanggar Peraturan Komunitas Shopee.'
            usersalah = 'Akun dan/atau password yang Anda masukkan salah. Mohon coba kembali.'
            error_message = error_message.replace(banned, 'Banned F02')
            error_message = error_message.replace(usersalah, 'Username/Password salah')
            writers.writelines(f"{userName}|{password}|{error_message}\n")
            writers.close()
            driver.quit()
            return False
        else:
            return False

    driver.find_elements_by_xpath('//*[@class="shopee-popover__ref"]/p')
    sel = Selector(text=driver.page_source)
    product_name = sel.xpath('//*[@class="shopee-popover__ref"]/p/text()').extract()
    product_sell = sel.xpath('//*[@class="product-list-item__td product-variation__sales"]/div/text()').extract()
    for (name, sell) in zip (product_name, product_sell):
        nameprod = name.strip()
        intsell = sell.strip()
        print('Scrape product : '+ nameprod +' With Sell : '+ intsell)
        writers = open('list product.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{userName}|{nameprod}|{'Penjualan : '+intsell}\n")
        writers.close()

def readProduct():
    username = open(r"username.txt", 'r', encoding='utf-8')
    readUsers = username.readlines()
    for readUser in readUsers:
        # read username to login
        user = readUser.strip()
        userName = user.split('|')[0]
        password = user.split('|')[1]
        continued = productSundul(userName, password)
        if not continued:
            continue

if __name__ == '__main__':
    readProduct()
