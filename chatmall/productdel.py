from selenium import webdriver
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

def delProduct(username, password):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(chrome_options=chrome_options)
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
    try:
        driver.find_element_by_xpath('//*[@class="guide-back"]').click()
        driver.implicitly_wait(10)
        print(username + ' Logged In !!')
    except:
        sel = Selector(text=driver.page_source)
        error_message = sel.xpath('//*[@class="shopee-alert-title"]/text()').extract_first().strip()
        print(error_message)
        writers = open('Product Delete.txt', 'a+', encoding = "utf-8")
        writers.writelines(f"\n{username}|{password}|{error_message}")
        writers.close()
        driver.quit()
        return False
        
    driver.find_elements_by_xpath('//*[@class="product-meta-item"]/span[text()="0"]')
    driver.implicitly_wait(5)
    sel = Selector(text=driver.page_source)
    views = driver.find_elements_by_xpath('//*[@class="product-meta-item"]/span[text()="0"]')
    count_view = sel.xpath('//*[@class="product-meta-item"]/span[text()="0"]/text()').extract_first()
    row = len(views)
    if row != 0:
        print('Siap dihapus dari '+ str(row) +'product')
    else:
        print('tidak ada product yang dihapus')
        driver.quit()
        return False

    view = views[0]
    view.find_element_by_xpath('//*[@class="shopee-checkbox__indicator"]').click()
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@class="delete-button shopee-button shopee-button--normal"]').click()
    driver.implicitly_wait(20)
    
    driver.find_elements_by_xpath('//*[@class="shopee-modal__footer-buttons"]/button')[1]
    driver.implicitly_wait(20)
   
    product_delete = driver.find_element_by_xpath('//*[@class="src-containers-modals---name--29JT9"]')
    
    sel = Selector(text=driver.page_source)
    product_delete = sel.xpath('//*[@class="src-containers-modals---name--29JT9"]/text()').extract_first().strip()
    localtime = time.asctime(time.localtime(time.time())).split()
    mounth = localtime[1]
    date = localtime[2]
    year = localtime[4]
    clock = localtime[3]

    writers = open('Product Delete.txt', 'a+', encoding = "utf-8")
    writers.writelines(f"\n{username}|{password}|{product_delete}|{mounth}-{date}-{year} {clock}")
    writers.close()
        
    driver.quit()


def main():
    username = open(r"username.txt", "r")
    reads = username.readlines()
    for read in reads:
        akun = read.strip()
        username = akun.split("|")[0]
        password = akun.split("|")[1]
        continued = delProduct(username, password)
        if not continued:
            continue
            print("Return Gagal Login!!")

if __name__ == '__main__':
    main()