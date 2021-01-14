from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector

def productSundul(userName, password, product1, product2):
    chrome_options = Options()
    chrome_options = chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
    driver.maximize_window()
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

    driver.find_element_by_xpath('//*[@class="guide-back"]').click()
    driver.implicitly_wait(10)

    driver.find_elements_by_xpath('//*[@class="view-modes"]/div')[0].click()
    driver.implicitly_wait(10)

    products = [product1, product2]
    for product in products:
        searchProduct = driver.find_element_by_xpath('//*[@class="shopee-input-group"]/span[2]//input')
        searchProduct.send_keys(product)
        searchProduct.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        # button more
        driver.find_element_by_xpath('//*[@class="product-action"]/div').click()
        driver.implicitly_wait(10)
        # boost product
        driver.find_element_by_xpath('//*[@class="shopee-popper dropdown-menu"]/ul/li[5]').click()

def readProduct():
    username = open(r"username.txt", 'r', encoding='utf-8')
    readUsers = username.readlines()
    for readUser in readUsers:
        user = readUser.strip()
        userName = user.split('|')[0]
        password = user.split('|')[1]
        products = open(r"product.txt", "r", encoding="utf-8")
        reads = products.readlines()
        for read in reads:
            product = read.strip()
            product1 = product.split("|")[0]
            product2 = product.split("|")[1]
            # product3 = product.split("|")[2]
            # product4 = product.split("|")[3]
            # product5 = product.split("|")[4]
            productSundul(userName, password, product1, product2)

if __name__ == '__main__':
    readProduct()
