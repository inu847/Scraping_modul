from selenium import webdriver
from parsel import Selector
from time import sleep
import parameters
import csv

def webchat(username):
    writer = csv.writer(open(parameters.result_file, 'w'))
    writer.writerow(['chat_from', 'chat_me', 'chat_buyer'])

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://seller.shopee.co.id/webchat/conversations')
    sleep(5)

    user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
    user.send_keys(username)
    sleep(3)

    passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
    passwd.send_keys(parameters.password)
    sleep(3)
    driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()
    sleep(5)

    # API BUYER CHAT = https://seller.shopee.co.id/webchat/api/v1.2/conversations/329442619095935409/messages?shop_id=219568618&offset=0&limit=20&direction=older&_s=4&_uid=0-219572657&_v=4.7.0&csrf_token=nrrq%2Fz9YEeuWAsy7%2Fl4BQg%3D%3D
    # LEN CHAT BUYER
    buyers = driver.find_elements_by_xpath('//*[@class="z8iJb5JoTh "]')
    for buyer in buyers:
        buyer.click()
        sleep(3)

        sel = Selector(text=driver.page_source)
        chat_from = sel.xpath('//*[@class="_34iAGBNPqd"]/text()').extract_first()
        chat_me = sel.xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl _3oQWa8rdLlo8Vgb5aY_iJC"]/text()').extract()
        chat_buyer = sel.xpath('//pre[@class="_2Zb8khbVxMFlHDDD2kMhKl"]/text()').extract()
        # product_name = sel.xpath('//*[@class="_2d5PdwXD15 _1I-Gx-uQ_G"]/text()').extract_first()
        # product_price = sel.xpath('//*[@class="_2tIduzSqLM _2rEqItiXyt"]/text()').extract_first().split('Rp ')[1]

        print('/n')
        print(chat_from)
        print(chat_me)
        print(chat_buyer)
        # print(product_name)
        # print(product_price)
        print('/n')

        writer.writerow([chat_from, chat_me, chat_buyer])

    driver.quit()

def main():
  for username in parameters.email:
    webchat(username)

if __name__ == '__main__':
    main()


