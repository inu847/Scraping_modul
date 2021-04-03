from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector
import requests
import json
import subprocess
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

def scrap(keywoard):
    proxies = {
        'http': 'socks5://127.0.0.1:9050',
        'https': 'socks5://127.0.0.1:9050'
    }
    # try:
    for newest in range(0,100000,50):
        try:
            URL = 'https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword='+str(keywoard)+'&limit=50&newest='+str(newest)+'&order=desc&page_type=search&version=2'
            shopeeId = requests.get(URL)
        except:
            print('Finished Scrap in This Category')
            return False
            
        #shopeeId = requests.get(URL)
        datas = shopeeId.json()
        arrs = datas['items']
        print(URL)
        
            
        for arr in arrs:
            shopid = arr['shopid']

            print('Shopee Id : '+ str(shopid))
            URLid = 'https://shopee.co.id/api/v4/product/get_shop_info?shopid='+str(shopid)
            data = requests.get(URLid)
            dataJson = data.json()
            username = dataJson['data']['account']['username']
            follower_count = dataJson['data']['follower_count']
            print("Username "+username+" Following "+str(follower_count))
                
            if follower_count < 200:
                writers = open('status/gmail.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{shopid}|{username}|{follower_count}\n")
                writers.close()
                writers = open('status/yahoo.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{shopid}|{username}|{follower_count}\n")
                writers.close()
                writers = open('status/results.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{shopid}|{username}|{follower_count}\n")
                writers.close()
            else:
                writers = open('status/user supplier.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{shopid}|{username}|{follower_count}\n")
                writers.close()
                writers = open('status/results.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{shopid}|{username}|{follower_count}\n")
                writers.close()
            
    #except:
    #    print("Cannot Activated Tor, Please Check IP socks5")
        
def scrapByKeywoard():
    #subprocess.Popen(['tor_proxy/Tor/tor.exe'])
    sleep(3)
    urls = open(r"ShopeeKeywoard.txt", "r")
    keywoards = urls.readlines()
    for key in keywoards:
        keywoard = key.replace(' ', '%20')
        keywoard = key.replace('&', '%26')
        keywoard = key.replace('-', '%20')
        continued = scrap(keywoard)
        if not continued:
            continue
        
def status(user, i, length):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://mall.shopee.co.id/buyer/login')
    driver.implicitly_wait(30)
    try:    
        username = driver.find_element_by_name('loginKey')
        username.send_keys(user + "@gmail.com")
        driver.implicitly_wait(30)
        
        password = driver.find_element_by_name('password')
        password.send_keys('Semogaberkah')
        driver.implicitly_wait(30)
    except:
        print('[ ERROR ]__main__: Alert!, Error Connection!!')
        driver.quit()
        return status(user, i, length)
        
    password.send_keys(Keys.RETURN)
    
    try:
        driver.implicitly_wait(10)
        driver.find_elements_by_xpath('//*[@class="_3mi2mp"]')
    
        print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
        sel = Selector(text=driver.page_source)
        label_supplier = sel.xpath('//*[@class="_3mi2mp"]/text()').extract_first()
        print(label_supplier)
    except:
        print('Logged In Shopee!!')
        driver.quit()
        return False
        
    if (label_supplier == 'Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?'):
        not_null = label_supplier.replace('Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?', 'NOT NULL')
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t" + not_null)
        writers = open('status/results.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{not_null}\n")
        writers.close()
    elif (label_supplier == 'Akun dan/atau password Anda salah, silakan coba lagi'):
        null = label_supplier.replace('Akun dan/atau password Anda salah, silakan coba lagi', 'NULL')
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t" + null)
        writers = open('status/gmail.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}|{null}\n")
        writers.close()
        writers = open('status/results.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{null}\n")
        writers.close()
        
    try:
        driver.implicitly_wait(30)
        driver.get('https://mall.shopee.co.id/buyer/login')
        driver.implicitly_wait(30)
        
        username = driver.find_element_by_name('loginKey')
        username.send_keys(user + "@yahoo.com")
        driver.implicitly_wait(30)
        
        password = driver.find_element_by_name('password')
        password.send_keys('Semogaberkah')
        driver.implicitly_wait(30)
        
        password.send_keys(Keys.RETURN)
        
        try:
            driver.implicitly_wait(30)
            driver.find_elements_by_xpath('//*[@class="_3mi2mp"]')
        except:
            print('Logged In Shopee!!')
            return False
        
        sel = Selector(text=driver.page_source)
        label_supplier = sel.xpath('//*[@class="_3mi2mp"]/text()').extract_first()
        not_null = label_supplier.replace('Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?', 'NOT NULL')
        null = label_supplier.replace('Akun dan/atau password Anda salah, silakan coba lagi', 'NULL')
        if (label_supplier == 'Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?'):
            print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t" + not_null)
            writers = open('status/results.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@yahoo.com|{not_null}\n")
            writers.close()
        elif (label_supplier == 'Akun dan/atau password Anda salah, silakan coba lagi'):
            print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t" + null)
            writers = open('status/yahoo.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}|{null}\n")
            writers.close()
            writers = open('status/results.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@yahoo.com|{null}\n")
            writers.close()
    except:
        pass
    
    driver.quit()

#main() getStatusUserShopee
def getstatus():
    user = open(r"user.txt", "r")
    reads = user.readlines()
    length = len(reads)
    
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[0]
        continued = status(user, i, length)
        if not continued:
            continue
        elif continued:
            return continued
            
def gmail(user, i, length, driver):
    driver.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')  
    driver.implicitly_wait(30)
    try:    
        username = driver.find_element_by_name('Username')
        username.send_keys(user)
        driver.implicitly_wait(30)
    except:
        print('[ ERROR ]__main__: Alert!, Error Connection!!')
        driver.quit()
        return gmail(user, i, length, driver)
         
    driver.find_element_by_name('Passwd').click()
    driver.implicitly_wait(3)
    print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
    
    try:
        driver.find_element_by_xpath('//*[@class="o6cuMc"]')
        sel = Selector(text=driver.page_source)
        status = sel.xpath('//*[@class="o6cuMc"]/text()').extract_first()
        result = status.replace(status, 'NOT NULL')
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t", result)
        writers = open('status/not_null.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{result}\n")
        writers.close() 
    except:
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t Null")
        writers = open('status/resultsgmail.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|NULL\n")
        writers.close()
        writers = open('status/null.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|NULL\n")
        writers.close()

#main() gmailChecker
def gmailChecker():
    user = open(r"status/gmail.txt", "r")
    reads = user.readlines()
    length = len(reads)
    
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[1]
        continued = gmail(user, i, length, driver)
        if not continued:
            continue
        elif continued:
            return continued

def yahoo(user, i, length, driver):
    driver.get('https://login.yahoo.com/account/create')
    driver.implicitly_wait(30)
    try:    
        username = driver.find_element_by_name('yid')
        username.send_keys(user)
        driver.implicitly_wait(10)
    except:
        print('[ ERROR ]__main__: Alert!, Error Connection!!')
        driver.quit()
        return yahoo(user, i, length, driver)
        
    driver.find_element_by_name('password').click()
    driver.implicitly_wait(5)
    print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
    try:
        driver.find_element_by_xpath('//*[@class="oneid-error-message"]')
        sel = Selector(text=driver.page_source)
        status = sel.xpath('//*[@class="oneid-error-message"]/text()').extract_first().strip()
        result = status.replace(status, 'NOT NULL')
        print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t Not Null")
        writers = open('status/not_null.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{result}\n")
        writers.close() 
    except:
        print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t Null")
        writers = open('status/resultsYahoo.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@yahoo.com|NULL\n")
        writers.close()
        writers = open('status/null.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@yahoo.com|NULL\n")
        writers.close()

#main() yahooChecker
def yahooChecker():
    user = open(r"status/yahoo.txt", "r")
    reads = user.readlines()
    length = len(reads)
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[1]
        continued = yahoo(user, i, length, driver)
        if not continued:
            continue
        elif continued:
            return continued

def detailUser(username, URL, i, length, driver):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver.get(URL)
    driver.implicitly_wait(10)
    print("[ INFO ]__main__: Progress ", i ,'/', length )
    print("[ INFO ]__main__: Progress with username:", username)
    try:
        driver.find_elements_by_xpath('//*[@class="shopee-search-user-seller-info-item__primary-text"]')
        sel = Selector(text=driver.page_source)
        speckMall = sel.xpath('//*[@class="shopee-search-user-seller-info-item__primary-text"]/text()').extract()
        for (speck, i) in zip ( speckMall, range(1, len(speckMall)) ):
            if i == 1:
                print("[ INFO ]__main__: Product ", speck )
                writers = open('status/product.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|Product : {speck}")
                writers.close()
            elif i == 2:
                print("[ INFO ]__main__: Penilaian ", speck )
                writers = open('status/product.txt', 'a+', encoding="utf-8")
                writers.writelines(f"|Penilaian : {speck}")
                writers.close()
            elif i == 3:
                print("[ INFO ]__main__: Performa ", speck )
                writers = open('status/product.txt', 'a+', encoding="utf-8")
                writers.writelines(f"|Performa : {speck}")
                writers.close()
                
        driver.implicitly_wait(10)       
        driver.find_elements_by_xpath('//*[@class="shopee-search-user-item__follow-count-number"]')
        following = sel.xpath('//*[@class="shopee-search-user-item__follow-count-number"]/text()').extract_first()
        print("[ INFO ]__main__: Following ", following )
        writers = open('status/product.txt', 'a+', encoding="utf-8")
        writers.writelines(f"|Following : {following}\n")
        writers.close()
    except:
        print('[ ALERT ]__main__:error connection!')        

#main() DetailUser
def productcek():
    gmails = open(r"status/resultsgmail.txt", "r")
    gmail = gmails.readlines()
    lengthgmail = len(gmail)
    
    yahoos = open(r"status/resultsyahoo.txt", "r")
    yahoo = yahoos.readlines()
    lengthyahoo = len(yahoo)
    
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    print('Enter Options:\n1. Gmail\n2. Yahoo\n3. Gmail And Yahoo!')
    choice = str(input('Input Choice : '))
    if (choice == '1'):
        writers = open('status/product.txt', 'a+', encoding="utf-8")
        writers.writelines("=============================================== Gmail ====================================================\n")
        writers.close()
        
        for (read, i) in zip (gmail, range(1, lengthgmail)):
            akun = read.strip()
            username = akun.split("|")[0]
            user = username.split('@')[0]
            URL = 'https://shopee.co.id/search?keyword=' + user
            detailUser(username, URL, i, lengthgmail, driver)
    elif (choice == '2'):
        writers = open('status/product.txt', 'a+', encoding="utf-8")
        writers.writelines("=============================================== Yahoo ====================================================\n")
        writers.close()    
        for (read, i) in zip (yahoo, range(1, lengthyahoo)):
            akun = read.strip()
            username = akun.split("|")[0]
            user = username.split('@')[0]
            URL = 'https://shopee.co.id/search?keyword=' + user
            detailUser(username, URL, i, lengthyahoo, driver)  
    elif (choice == '3'):
        writers = open('status/product.txt', 'a+', encoding="utf-8")
        writers.writelines("=============================================== Gmail ====================================================\n")
        writers.close()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        
        for (read, i) in zip (gmail, range(1, lengthgmail)):
            akun = read.strip()
            username = akun.split("|")[0]
            user = username.split('@')[0]
            URL = 'https://shopee.co.id/search?keyword=' + user
            detailUser(username, URL, i, lengthgmail, driver)
            
        writers = open('status/product.txt', 'a+', encoding="utf-8")
        writers.writelines("=============================================== Yahoo ====================================================\n")
        writers.close()    
        for (read, i) in zip (yahoo, range(1, lengthyahoo)):
            akun = read.strip()
            username = akun.split("|")[0]
            user = username.split('@')[0]
            URL = 'https://shopee.co.id/search?keyword=' + user
            detailUser(username, URL, i, lengthyahoo, driver)
    else:
        print('Tidak Ada Opsi!!')
        
def mail(user, i, length, driver, drivers):
    driver.get('https://shopee.co.id/buyer/login/reset')
    driver.implicitly_wait(30)
    
    print("[ INFO ]__main__: In Progress "+ str(i) + "/" + str(length) )
    
    try:
        email = driver.find_element_by_xpath('//*[@autocomplete="username"]')
        email.send_keys(user)
        email.send_keys(Keys.RETURN)
        driver.implicitly_wait(30)
        driver.find_element_by_xpath('//*[@class="_2sB0oN"]')
        driver.implicitly_wait(30)
        try:
            sleep(1)
            imgCaptcha = driver.find_element_by_xpath('//*[@class="_25_r8I"]/img')
            driver.execute_script("return arguments[0].scrollIntoView();", imgCaptcha)
            sel = Selector(text=driver.page_source)
            imagesCaptcha = sel.xpath('//*[@class="_25_r8I"]/img/@src').extract_first()
            drivers.get(imagesCaptcha)
        except:
            print("[ ERRr ]__main__: captcha not found!! ")
            return mail(user, i, length, driver)
    except:
        return mail(user, i, length, driver, drivers)    
        
    captcha = driver.find_element_by_xpath('//*[@autocomplete="off"]')
    inputCaptcha = input("Masukkan Capthcha: ")
    if not inputCaptcha:
        return mail(user, i, length, driver, drivers)

    captcha.send_keys(inputCaptcha)
    captcha.send_keys(Keys.RETURN)
    driver.implicitly_wait(3)
    
    try:
        driver.find_element_by_xpath('//*[@class="stardust-icon stardust-icon-email-with-lock _1lm8Wr"]')
        sel = Selector(text=driver.page_source)
        status = sel.xpath('//*[@class="M5j680"]/div/text()').extract_first()
        print(status)
        print("[ INFO ]__main__: Success")
        writers = open('status/userReady.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}|Terdaftar\n")
        writers.close()
    except:
        print("[ INFO ]__main__: Invalid!!")

def send_email():
    mobile_emulation = {

        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },

        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }

    chrome_options = Options()

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(chrome_options = chrome_options)
    drivers = webdriver.Chrome()
    user = open(r"status/product.txt", "r")
    reads = user.readlines()
    length = len(reads)
    
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[0]
        continued = mail(user, i, length, driver, drivers)
        if not continued:
            continue
            
def holiday_toko(user, i, length, password1, password2):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://seller.shopee.co.id/portal/settings/basic/shop')
    driver.implicitly_wait(30)
    print("[ INFO ]__main__: In Progress "+ str(i) + "/" + str(length) )
    try:
        username = driver.find_element_by_xpath('//*[@autocomplete="username"]')
        username.send_keys(user)
        driver.implicitly_wait(30)
                
        password = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
        password.send_keys(password1)
        password.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        #try:
        #    driver.find_element_by_xpath('//*[@class="shopee-react-button EntryLayout_guideBtn__3bR8I shopee-react-button--primary shopee-react-button--normal"]').click()
        #except:
        #    pass
        try:
            driver.find_element_by_xpath('//*[@class="onboarding-tips-button shopee-button shopee-button--link shopee-button--normal"]').click()
            driver.implicitly_wait(30)
            print("[ AUTH ]__main__: "+ user +" logged in" )
            driver.find_elements_by_xpath('//*[@class="shopee-switch shopee-switch--close shopee-switch--normal"]')[1].click()
            driver.implicitly_wait(30)
            driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--normal"]').click()
            driver.implicitly_wait(30)
            driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--normal"]').click()
            
            localtime = time.asctime(time.localtime(time.time())).split()
            mounth = localtime[1]
            date = localtime[2]
            year = localtime[4]
            clock = localtime[3]
            print(f"[ INFO ]__main__: Toko Libur : {mounth}-{date}-{year} {clock}")
            writers = open('status/tokolibur.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}|Toko Libur|{mounth}-{date}-{year} {clock}\n")
            writers.close()
        except:
            print("[ ALERT ]__main__: Kena Captha")
            writers = open('status/tokolibur.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}|Kena Captha\n")
            writers.close()
            sleep(10)
            return False
    except:
        username = driver.find_element_by_xpath('//*[@autocomplete="username"]')
        username.send_keys(user)
        driver.implicitly_wait(30)
                
        password = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
        password.send_keys(password2)
        password.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        try:
            driver.find_element_by_xpath('//*[@class="onboarding-tips-button shopee-button shopee-button--link shopee-button--normal"]').click()
            driver.implicitly_wait(30)
            print("[ AUTH ]__main__: "+ user +" logged in" )
            driver.find_elements_by_xpath('//*[@class="shopee-switch shopee-switch--close shopee-switch--normal"]')[1].click()
            driver.implicitly_wait(30)
            driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--normal"]').click()
            driver.implicitly_wait(30)
            driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--normal"]').click()

            localtime = time.asctime(time.localtime(time.time())).split()
            mounth = localtime[1]
            date = localtime[2]
            year = localtime[4]
            clock = localtime[3]
            print(f"[ INFO ]__main__: Toko Libur : {mounth}-{date}-{year} {clock}")
            writers = open('status/tokolibur.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}|Toko Libur|{mounth}-{date}-{year} {clock}\n")
            writers.close()
        except:
            writers = open('status/tokolibur.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}|Processing Failed\n")
            writers.close()
            print("[ ALERT ]__main__: processing Failed" )
            return False
            
    driver.quit()
def libur_toko():
    user = open(r"username.txt", "r")
    reads = user.readlines()
    length = len(reads)
    password1 = input("Input Password 1 : ")
    password2 = input("Input Password 2 : ")
    
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[0]
        continued = holiday_toko(user, i, length, password1, password2)
        if not continued:
            continue

            
def main():   
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("data/config-cd7413190612.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("config").sheet1
    datas = sheet.get_all_records()
    for data in datas:
        email = data['Email']
        password = data['Password']
        userAgent = data['User Agent']
        status = data['Status']
        
    user = open(r"data/config.json", "r")
    dataJsons = json.load(user)
    emailConfig = dataJsons['lisensi']['email']
    passwordConfig = dataJsons['lisensi']['pwd']
    userAgentConfig = dataJsons['lisensi']['user-agent']
        
    if email == emailConfig and password == passwordConfig and userAgent == userAgentConfig and status == 'Active':
        print('Enter Options:\n1. Get User (API)\n2. Get Status User (Innactive)\n3. Gmail Checker!\n4. Yahoo.Checker\n5. Cek Detail User\n6. Cek User Activated\n7. Libur Toko')
        choice = str(input('Input Choice : '))
        if choice == '1':
            if __name__ == '__main__':
                os.system('cls')
                scrapByKeywoard()
        elif choice == '2':
            print("Bot Not Working")
            main()
            #if __name__ == '__main__':
            #    getstatus()
        elif choice == '3':
            if __name__ == '__main__':
                os.system('cls')
                gmailChecker()
        elif choice == '4':
            if __name__ == '__main__':
                os.system('cls')
                yahooChecker()
        elif choice == '5':
            if __name__ == '__main__':
                os.system('cls')
                productcek()
        elif choice == '6':
            if __name__ == '__main__':
                os.system('cls')
                send_email()
        elif choice == '7':
            if __name__ == '__main__':
                os.system('cls')
                libur_toko()
        else:
            print('Tidak Ada Opsi!!')
            main()
    elif status != 'Active':
        print('Login Failed!! Your Config non-active')
        sleep(3)
    else:
        print('Login Failed!! Check your config')
        sleep(3)

main()