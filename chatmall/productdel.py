from selenium import webdriver
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
import time

def delProduct(username, password):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    # driver.minimize_window()
    driver.get('https://seller.shopee.co.id/portal/product/list/all')
    driver.implicitly_wait(30)

    user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
    user.send_keys(username)
    driver.implicitly_wait(20)

    passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
    passwd.send_keys(password)
    driver.implicitly_wait(20)
    
    driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()
    driver.implicitly_wait(30)

    driver.find_element_by_xpath('//*[@class="guide-back"]').click()
    driver.implicitly_wait(20)

    logon = driver.find_element_by_xpath('//*[@class="account-name"]')
    if logon:
        print(username + ' Logged In !!')
    else:
        print('Gagal Login cek username password')
        driver.quit()
        main()


    try:
        driver.find_elements_by_xpath('//*[@class="product-meta-item"]/span[text()="0"]')
        driver.implicitly_wait(5)
    except:
        pass

    views = driver.find_elements_by_xpath('//*[@class="product-meta-item"]/span[text()="0"]')
    driver.implicitly_wait(20)

    view = views[0]
    view.find_element_by_xpath('//*[@class="shopee-checkbox__indicator"]').click()
    driver.implicitly_wait(20)
        
    driver.find_element_by_xpath('//*[@class="delete-button shopee-button shopee-button--normal"]').click()
    driver.implicitly_wait(20)

    driver.find_element_by_xpath('//*[@class="src-containers-modals---name--29JT9"]')
    driver.implicitly_wait(20)

    # driver.find_elements_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--normal"]')[6].click()
    # driver.implicitly_wait(20)
    
    sel = Selector(text=driver.page_source)
    product_delete = sel.xpath('//*[@class="src-containers-modals---name--29JT9"]/text()').extract_first().strip()
    localtime = time.asctime(time.localtime(time.time())).split()
    mounth = localtime[1]
    date = localtime[2]
    year = localtime[4]
    clock = localtime[3]
    time = (f"{mounth}-{date}-{year} {clock}")

    # print(product_delete)

    writers = open('Product Delete.txt', 'a+', encoding = "utf-8")
    writers.writelines(f"\n{username}|{password}|{product_delete}|{time}")
    writers.close()
        
    driver.quit()


def main():
    username = open(r"username.txt", "r")
    reads = username.readlines()
    for read in reads:
        akun = read.strip()
        username = akun.split("|")[0]
        password = akun.split("|")[1]
        delProduct(username, password)

if __name__ == '__main__':
    main()