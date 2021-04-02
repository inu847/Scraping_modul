from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import requests
import os
import subprocess
import string
import random

def scrap(driver, categoriesUrl, idCategory, currentUrl):
    for next_page in range(1, 500):
        # URLstar = "http://localhost/aliexpress-curl/" + str(currentUrl)+ ".php?trafficChannel=main&catName=" + str(currentUrl) + "&CatId=" + str(idCategory) + "&ltype=wholesale&isFavorite=y&SortType=default&page="+ str(next_page)
        URLrandom = str(currentUrl)+ "?trafficChannel=main&catName=dresses&CatId=200003482&ltype=wholesale&SortType=default&page="+str(next_page)
        driver.get(URLrandom)               
        try:
            for lenCategory in range(1, 15):
                for lenLi in range(1,4):
                    inCategory = driver.find_element_by_xpath('//*[@class="list-items"]/div'+ str([lenCategory]) +'/li'+ str([lenLi]) +'/div/div[2]/div/div/a')
                    driver.execute_script("return arguments[0].scrollIntoView();", inCategory)
        except:
            print("[ ERROR ]__main__: Failed Parsing")
            break
        try:
            productTitle = driver.find_elements_by_css_selector('.item-title-wrap>a')
            # productImage = driver.find_elements_by_css_selector('.place-container>a>img')
            # ratings = driver.find_elements_by_css_selector('.rating-value')
            suppliers = driver.find_elements_by_css_selector('.item-store-wrap>a[title]')
            print(len(productTitle))
            for (title, supplier) in zip (productTitle, suppliers):
                resultsTitle = title.text
                # resultsRating = rating.text
                resultsSupplier = supplier.text

                print(resultsTitle +" "+ resultsSupplier.upper())
                writers = open('grabCategoriesRandom.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{categoriesUrl}|{resultsTitle}\n")
                writers.close()
        except:
            print("Parsing failed")
        print(driver.current_url)

def grabAliexpress():
    # subprocess.Popen(['tor_proxy/Tor/tor.exe'])
    # PROXY = "socks5://127.0.0.1:9050"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--lang=id")
    # prefs = {
    #     "translate_whitelists": {"en":"id"},
    #     "translate":{"enabled":"true"}
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome()
    urls = open(r"urlCategories.txt", "r")
    reads = urls.readlines()
    
    for read in reads:
        url = read.strip()
        categoriesUrl = url.split("|")[0]
        idCategory = url.split("|")[1]
        currentUrl = url.split("|")[2]
        
        scrap(driver, categoriesUrl, idCategory, currentUrl)

if __name__ == '__main__':
    grabAliexpress()
    