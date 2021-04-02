from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from parsel import Selector
import requests
import os
import subprocess

def scrap(driver, categoriesUrl, currentUrl, categoryURL, category, urlCategory, idc):
    for next_page in range(1, 60):
        # URLstar = "https://www.aliexpress.com/af/category/" + idc + ".html?trafficChannel=af&catName=" + categoryURL.lower() + "&CatId=" + idc + "&ltype=wholesale&isFavorite=y&SortType=default&page="+ str(next_page) + "&isFavorite=y"
        URLrandom = "https://www.aliexpress.com/af/category/" + idc + ".html?trafficChannel=af&catName=" + categoryURL.lower() + "&CatId=" + idc + "&ltype=affiliate&SortType=default&page="+ str(next_page) + "&isrefine=y"
        driver.get(URLrandom)
        driver.implicitly_wait(20)
            # try:
                # Sub Categories
                # if driver.current_url == URLrandom:
                #     try:
                #         idSubCategory = sel.xpath('//*[@class="child-menu"]/li/@ae_object_value').extract()
                #         subCategories = sel.xpath('//*[@target="_self"]/text()').extract()
                #         urlSubCategories = sel.xpath('//*[@class="child-menu"]/li/a/@href').extract()
                #         # keywoards = sel.xpath('//*[@class="child-menu"]/li/@data-spm-anchor-id').extract()
                #         for (subcategory, subUrlCategory, subIdc) in zip (subCategories, urlSubCategories, idSubCategory):
                #             print('[ INFO ]__main__: ' + categoriesUrl)
                #             print('[ INFO ]__main__: ' + subcategory + " " + subIdc)
                #             print('[ INFO ]__main__: https:' + subUrlCategory)
                #             # URL = 'https:'+urlCategory+'?spm='+keywoard
                #             subCategoryURL = subcategory.replace("'", "")
                #             subCategoryURL = subcategory.replace(' & ', '-')
                #             for next_page in range(1, 60):
                #                 # URLstar = "https://www.aliexpress.com/af/category/" + subIdc + ".html?trafficChannel=af&catName=" + subCategoryURL.lower() + "&CatId=" + subIdc + "&ltype=wholesale&isFavorite=y&SortType=default&page="+ str(next_page) + "&isFavorite=y"
                #                 URLrandom = "https://www.aliexpress.com/af/category/" + subIdc + ".html?trafficChannel=af&catName=" + subCategoryURL.lower() + "&CatId=" + subIdc + "&ltype=affiliate&SortType=default&page="+ str(next_page) + "&isrefine=y"
                #                 driver.get(URLrandom)
                #                 driver.implicitly_wait(20)
                #                 try:
                #                     for lenSubCategory in range(1, 15):
                #                         for subLenLi in range(1,4):
                #                             inSubCategory = driver.find_element_by_xpath('//*[@class="list-items"]/div'+ str([lenSubCategory]) +'/li'+ str([subLenLi]) +'/div/div[2]/div/div/a')
                #                             driver.execute_script("return arguments[0].scrollIntoView();", inSubCategory)
                #                 except:
                #                     print('not subcategories')
                #                 driver.implicitly_wait(5)
                #                 productSubTitle = driver.find_elements_by_css_selector('.item-title-wrap>a')
                #                 subratings = driver.find_elements_by_css_selector('.rating-value')
                #                 print(len(productSubTitle))
                #                 for (subTitle, subRating) in zip (productSubTitle, subratings):
                #                     resultsSubTitle = subTitle.text
                #                     resultsSubRating = subRating.text

                #                     print(resultsSubTitle + " ✯" + str(resultsSubRating))
                #                     writers = open('grabCategoriesRandomtest.txt', 'a+', encoding="utf-8")
                #                     writers.writelines(f"\t{subcategory}|{subIdc}|{resultsSubTitle}|✯ {resultsSubRating}\n")
                #                     writers.close()
                    
                #                     print(driver.current_url)
                #     except:
                #         print('not subcategories')
                # else:
                #     print('not subcategories')
        try:
            for lenCategory in range(1, 15):
                for lenLi in range(1,4):
                    inCategory = driver.find_element_by_xpath('//*[@class="list-items"]/div'+ str([lenCategory]) +'/li'+ str([lenLi]) +'/div/div[2]/div/div/a')
                    driver.execute_script("return arguments[0].scrollIntoView();", inCategory)
        except:
            print("[ ERROR ]__main__: Failed Parsing")
            break

        driver.implicitly_wait(5)
        productTitle = driver.find_elements_by_css_selector('.item-title-wrap>a')
        # productImage = driver.find_elements_by_css_selector('.place-container>a>img')
        ratings = driver.find_elements_by_css_selector('.rating-value')
        print(len(productTitle))
        for (title, rating) in zip (productTitle, ratings):
            resultsTitle = title.text
            resultsRating = rating.text
                # image = images.get_attribute('src')
                # picture = image.replace('_220x220xz.jpg_.webp', '')

                # try: 
                #     os.mkdir('imagesAliexpress') 
                # except: 
                #     pass

            try:
                    # response = requests.get(picture)
                    # file = open("imagesAliexpress/"+resultsTitle+'.jpg', "wb")
                    # file.write(response.content)
                    # file.close()

                print(resultsTitle + " ✯" + str(resultsRating))
                writers = open('grabCategoriesRandomtest.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{categoriesUrl}|{category}|{idc}|{resultsTitle}|✯ {resultsRating}\n")
                writers.close()
            except:
                print("file already exists")
                
        print(driver.current_url)

def grabAliexpress():
    #subprocess.Popen(['tor_proxy/Tor/tor.exe'])
    #PROXY = "socks5://127.0.0.1:9050"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #chrome_options.add_argument('--proxy-server=%s' % PROXY)
    # chrome_options.add_argument("--lang=id")
    # prefs = {
    #     "translate_whitelists": {"en":"id"},
    #     "translate":{"enabled":"true"}
    # }
    # chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    urls = open(r"url.txt", "r")
    reads = urls.readlines()
    
    for read in reads:
        url = read.strip()
        categoriesUrl = url.split("|")[0]
        currentUrl = url.split("|")[1]
        # scrap(driver, categoriesUrl, currentUrl)
        driver.get(currentUrl)
        driver.implicitly_wait(30)
        driver.find_elements_by_xpath('//*[@target="_self"]')
        driver.implicitly_wait(30)
        
        sel = Selector(text=driver.page_source)
        idCategory = sel.xpath('//*[@class="child-menu"]/li/@ae_object_value').extract()
        categories = sel.xpath('//*[@target="_self"]/text()').extract()
        urlCategories = sel.xpath('//*[@class="child-menu"]/li/a/@href').extract()
        # keywoards = sel.xpath('//*[@class="child-menu"]/li/@data-spm-anchor-id').extract()
        for (category, urlCategory, idc) in zip (categories, urlCategories, idCategory):
            print('[ INFO ]__main__: ' + categoriesUrl)
            print('[ INFO ]__main__: ' + category + " " + idc)
            print('[ INFO ]__main__: https:' + urlCategory)
            # URL = 'https:'+urlCategory+'?spm='+keywoard
            categoryURL = category.replace("'", "")
            categoryURL = category.replace(' & ', '-')
            scrap(driver, categoriesUrl, currentUrl, categoryURL, category, urlCategory, idc)
if __name__ == '__main__':
    grabAliexpress()
    