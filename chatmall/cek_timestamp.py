from selenium import webdriver
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

def timestamp(username, password):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(20)
    driver.get('https://shopee.co.id/user/notifications/shopee')
    driver.implicitly_wait(20)

    user = driver.find_element_by_name("loginKey")
    user.send_keys(username)
    driver.implicitly_wait(20)

    passwd = driver.find_element_by_name("password")
    passwd.send_keys(password)
    driver.implicitly_wait(20)

    passwd.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)
    try:
        driver.find_element_by_xpath('//*[@class="navbar__username"]')
        print(username + ' Logged In !!')
        driver.implicitly_wait(5)
    except:
        sel = Selector(text=driver.page_source)
        error_message = sel.xpath('//*[@class ="_2d8JQY"]/text()').extract_first()
        f02 = error_message.replace(error_message, "Banned F02")
        print(f02)
        writers = open('notifications.txt', 'a+', encoding = "utf-8")
        writers.writelines(f"{username}|{password}|{f02}\n")
        writers.close()
        driver.quit()
        return False

    driver.find_element_by_xpath('//*[text()="akun kamu tidak dapat digunakan untuk mengikuti program Gratis Ongkir"]')
    sel = Selector(text=driver.page_source)
    notif = sel.xpath('//*[@class="_1U308K _1LCoBe"]')
    tidak_dapat_digunakan = notif.xpath('//*[text()="akun kamu tidak dapat digunakan untuk mengikuti program Gratis Ongkir"]/text()').extract_first()
    timestamp = sel.xpath('//*[@class="_1U308K _1LCoBe"]/div/p/text()').extract_first()

    if tidak_dapat_digunakan:
        print("Status akun : Username")
    else:
        driver.get('https://shopee.co.id/user/notifications/order')
        driver.implicitly_wait(10)
        driver.find_element_by_xpath('//*[text()="akun kamu tidak dapat digunakan untuk mengikuti program Gratis Ongkir"]')
        sel = Selector(text=driver.page_source)
        notif = sel.xpath('//*[@class="_1U308K _1LCoBe"]')
        tidak_bisa_digunakan = notif.xpath('//*[text()="akun kamu tidak dapat digunakan untuk mengikuti program Gratis Ongkir"]/text()').extract_first()
        username_akun = tidak_bisa_digunakan.replace(tidak_bisa_digunakan, "username")
        print("Status akun : "+ username_akun)
        writers = open('notifications.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{username}|{password}|{username_akun}|{timestamp}\n")
        writers.close()
        driver.quit()
        return False

    print("Timestamp : "+ timestamp)

    akun_username = tidak_dapat_digunakan.replace(tidak_dapat_digunakan, "username")
    writers = open('notifications.txt', 'a+', encoding = "utf-8")
    writers.writelines(f"{username}|{password}|{akun_username}|{timestamp}\n")
    writers.close()

    driver.quit()

def main():
    username = open(r"username.txt", "r")
    reads = username.readlines()
    for read in reads:
        akun = read.strip()
        username = akun.split("|")[0]
        password = akun.split("|")[1]
        continued = timestamp(username, password)
        if not continued:
            continue
        print("GAGAL LOGIN")

if __name__ == '__main__':
    main()