from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector

def productSundul(userName, password, product1, product2, product3, product4, product5):
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


    products = [product1, product2, product3, product4, product5]
    for product in products:
        searchProduct = driver.find_element_by_xpath('//*[@class="shopee-input-group"]/span[2]//input')
        searchProduct.send_keys(product)
        driver.implicitly_wait(10)
        searchProduct.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        sleep(2)
        driver.find_element_by_xpath('//*[text()="'+product+'"]')
        localtime = time.asctime(time.localtime(time.time())).split()
        mounth = localtime[1]
        date = localtime[2]
        year = localtime[4]
        clock = localtime[3]
        try:
            # button more
            driver.find_element_by_xpath('//*[@class="product-action"]/div').click()
            driver.implicitly_wait(10)
            # boost product
            driver.find_element_by_xpath('//*[@class="shopee-popper dropdown-menu"]/ul/li[5]').click()
            print("product sundul : "+ product)
        except:
            print("Gagal disundul")
            writers = open('product sundul.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{userName}|{product}|{'Failed'}|{mounth}-{date}-{year} {clock}\n")
            writers.close()

        driver.get('https://seller.shopee.co.id/portal/product/list/all?page=1')
        driver.implicitly_wait(5)

        writers = open('product sundul.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{userName}|{product}|{'Success'}|{mounth}-{date}-{year} {clock}\n")
        writers.close()

    driver.quit()

def readProduct():
    username = open(r"username.txt", 'r', encoding='utf-8')
    readUsers = username.readlines()
    products = open(r"product.txt", "r", encoding="utf-8")
    reads = products.readlines()
    for (readUser, read) in zip (readUsers, reads):
        # read username to login
        user = readUser.strip()
        userName = user.split('|')[0]
        password = user.split('|')[1]

        # read product to search boost
        product = read.strip()
        product1 = product.split("|")[0]
        product2 = product.split("|")[1]
        product3 = product.split("|")[2]
        product4 = product.split("|")[3]
        product5 = product.split("|")[4]
        continued = productSundul(userName, password, product1, product2, product3, product4, product5)
        if not continued:
            continue

if __name__ == '__main__':
    readProduct()
