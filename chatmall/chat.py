from selenium import webdriver
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
import parameters
import csv

def webchat(username, password):
    # writer = csv.writer(open(parameters.result_file, 'w'))
    # writer.writerow(['chat_from', 'chat_me', 'chat_buyer', 'product_name', 'product_price'])
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(20)
    # driver.minimize_window()
    driver.get('https://seller.shopee.co.id/webchat/conversations')
    driver.implicitly_wait(20)

    user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
    user.send_keys(username)
    driver.implicitly_wait(20)

    passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
    passwd.send_keys(password)
    driver.implicitly_wait(20)
    
    driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()
    driver.implicitly_wait(20)

    logon = driver.find_element_by_xpath('//*[@class="_3fBm1wELGG"]')
    if logon:
        print(username + ' success logon')
    else:
        print('Gagal Login cek username password')
        driver.quit()
        main()

    # API BUYER CHAT = https://seller.shopee.co.id/webchat/api/v1.2/conversations/329442619095935409/messages?shop_id=219568618&offset=0&limit=20&direction=older&_s=4&_uid=0-219572657&_v=4.7.0&csrf_token=nrrq%2Fz9YEeuWAsy7%2Fl4BQg%3D%3D
    # LEN CHAT BUYER
    buyers = driver.find_elements_by_xpath('//*[@class="z8iJb5JoTh "]')
    print('/n')
    print(len(buyers))
    print('/n')
    
    for buyer in buyers:
        buyer.click()
        driver.implicitly_wait(2)
        
        sel = Selector(text=driver.page_source)
        connection_error = sel.xpath('//*[@class="_2hgL8kwJb4E7a3ggdF9PMp"]')
        if connection_error:
            main()

        try:
            driver.find_elements_by_xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl _3oQWa8rdLlo8Vgb5aY_iJC"]')
            driver.implicitly_wait(2)
            driver.find_elements_by_xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl"]')
            driver.implicitly_wait(2)
            driver.find_elements_by_xpath('//*[@class="_2d5PdwXD15 _1I-Gx-uQ_G"]')
            driver.implicitly_wait(2)
            driver.find_elements_by_xpath('//*[@class="_2tIduzSqLM _2rEqItiXyt"]')
            driver.implicitly_wait(2)
            driver.find_elements_by_xpath('//*[@class="_1gEytIy7qKccGA5xfdWQVH"]')
            driver.implicitly_wait(2)
        except:
            pass
        
        sel = Selector(text=driver.page_source)
        chat_from = sel.xpath('//*[@class="_34iAGBNPqd"]/text()').extract_first()
        chat_me = sel.xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl _3oQWa8rdLlo8Vgb5aY_iJC"]/text()').extract()
        chat_buyer = sel.xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl"]/text()/following-sibling::*[@class="_3fF9tZdS-P  "]/text()').extract()
        product_name = sel.xpath('//*[@class="_2d5PdwXD15 _1I-Gx-uQ_G"]/text()').extract_first()
        product_price = sel.xpath('//*[@class="_2tIduzSqLM _2rEqItiXyt"]/text()').extract_first()
        url_image = sel.xpath('//a[@class="_1gEytIy7qKccGA5xfdWQVH"]/@href').extract_first()
        mssg_timestamp = sel.xpath('//div/[@class="_3fF9tZdS-P  "]/text()').extract_first()

        print('/n')
        print(chat_from)
        print(chat_me)
        print(chat_buyer)
        print(product_name)
        print(product_price)
        print(url_image)
        print('/n')

        # writer.writerow([chat_from, chat_me, chat_buyer, product_name, product_price])

    driver.quit()

def main():
    for username, password in zip (parameters.email, parameters.password):
            webchat(username, password)


if __name__ == '__main__':
    main()