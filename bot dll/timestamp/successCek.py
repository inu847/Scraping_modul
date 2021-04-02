from selenium import webdriver
from parsel import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep

def timestamp(username, password, length, i, insuccess):
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(20)
    driver.get('https://shopee.co.id/user/notifications/order')
    driver.implicitly_wait(20)
    
    try:
        user = driver.find_element_by_name("loginKey")
        user.send_keys(username)
        driver.implicitly_wait(20)

        passwd = driver.find_element_by_name("password")
        passwd.send_keys(password)
        driver.implicitly_wait(20)

        passwd.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        
        driver.find_element_by_xpath('//*[@class="navbar__username"]')
        driver.implicitly_wait(10)
            
        print("[ INFO ]__main__:In Progress "+ str(length) + "/" + str(i))
        print("[ INFO ]__main__:Success "+ str(insuccess))
        print("[ AUTH ]__main__:" + username + ' Logged In !!')
            
        notif = driver.find_elements_by_xpath('//*[@class="_1U308K _1LCoBe"]')
        sel = Selector(text=driver.page_source)
        notification = sel.xpath('//*[@class="_1U308K _1LCoBe"]/h1/text()').extract()
        if not notif:
            try:
                print('[ INFO ]__main__:Nothing Notification')
                print('[ INFO ]__main__:Redirect to https://shopee.co.id/user/notifications/shopee')
                driver.get('https://shopee.co.id/user/notifications/shopee')
                driver.implicitly_wait(20)
                notif = driver.find_elements_by_xpath('//*[@class="_1U308K _1LCoBe"]')
                sel = Selector(text=driver.page_source)
                notification = sel.xpath('//*[@class="_1U308K _1LCoBe"]/h1/text()').extract()
                timestamp = sel.xpath('//*[@class="_1U308K _1LCoBe"]/div/p/text()').extract()
                driver.implicitly_wait(10)
                for (status, results, time) in zip (notif, notification, timestamp):
                    driver.execute_script("return arguments[0].scrollIntoView();", status)
                    driver.implicitly_wait(20)
                    success = 'Aktivasi Hampir Selesai'
                    if results == success:
                        sel = Selector(text=driver.page_source)
                        
                        resultsSucccess = results.replace('Aktivasi Hampir Selesai', 'Success')
                        print("[ INFO ]__main__:Status akun : " + str(resultsSucccess))
                        print("[ INFO ]__main__:Timestamp : " + str(time))
                        writers = open('self_info/result.txt', 'a+', encoding="utf-8")
                        writers.writelines(f"{username}|{password}|{resultsSucccess}|{time}\n")
                        writers.close()
                        writers = open('self_info/success.txt', 'a+', encoding="utf-8")
                        writers.writelines(f"{username}|{password}|{resultsSucccess}|{time}\n")
                        writers.close()
                    else:
                        sel = Selector(text=driver.page_source)
                        timestampInvalid = sel.xpath('//*[@class="_1U308K _1LCoBe"]/div/p/text()').extract()
                        print("[ INFO ]__main__:Status akun : invalid")
                        print("[ INFO ]__main__:Timestamp : " + str(time))
                        writers = open('self_info/result.txt', 'a+', encoding="utf-8")
                        writers.writelines(f"{username}|{password}|invalid|{time}\n")
                        writers.close()
            except:
                print('Belum Ada Riwayat pendaftaran')
                writers = open('self_info/result.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|{password}|belum|{time}\n")
                writers.close()
                
        timestamp = sel.xpath('//*[@class="_1U308K _1LCoBe"]/div/p/text()').extract()
        driver.implicitly_wait(10)
        for (status, results, time) in zip (notif, notification, timestamp):
            driver.execute_script("return arguments[0].scrollIntoView();", status)
            driver.implicitly_wait(20)
            success = 'Aktivasi Hampir Selesai'
            if results == success:
                sel = Selector(text=driver.page_source)
                
                resultsSucccess = results.replace('Aktivasi Hampir Selesai', 'Success')
                print("[ INFO ]__main__:Status akun : " + str(resultsSucccess))
                print("[ INFO ]__main__:Timestamp : " + str(time))
                writers = open('self_info/result.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|{password}|{resultsSucccess}|{time}\n")
                writers.close()
                writers = open('self_info/success.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|{password}|{resultsSucccess}|{time}\n")
                writers.close()
            else:
                sel = Selector(text=driver.page_source)
                timestampInvalid = sel.xpath('//*[@class="_1U308K _1LCoBe"]/div/p/text()').extract()
                print("[ INFO ]__main__:Status akun : invalid")
                print("[ INFO ]__main__:Timestamp : " + str(time))
                writers = open('self_info/result.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{username}|{password}|invalid|{time}\n")
                writers.close()
                   
        print('')
        writers = open('self_info/result.txt', 'a+', encoding="utf-8")
        writers.writelines("\n")
        writers.close()
    except:
        sel = Selector(text=driver.page_source)
        error_message = sel.xpath('//*[@class ="_2d8JQY"]/text()').extract_first()
        f02 = error_message.replace("Akun sedang ditinjau karena alasan keamanan atau karena ada aktivitas yang melanggar Peraturan Komunitas Shopee.", "Banned F02")
        pwfalse = error_message.replace("Akun dan/atau password Anda salah, silakan coba lagi", "UserFalse")
        if error_message == "Akun sedang ditinjau karena alasan keamanan atau karena ada aktivitas yang melanggar Peraturan Komunitas Shopee.":
            print("[ ALERT ]__main__:" + f02)
            writers = open('self_info/banned.txt', 'a+', encoding = "utf-8")
            writers.writelines(f"{username}|{password}|{f02}\n")
            writers.close()
            writers = open('self_info/result.txt', 'a+', encoding = "utf-8")
            writers.writelines(f"{username}|{password}|{f02}\n")
            writers.close()
        elif error_message == "Akun dan/atau password Anda salah, silakan coba lagi":
            print("[ ALERT ]__main__:" + pwfalse)
            writers = open('self_info/banned.txt', 'a+', encoding = "utf-8")
            writers.writelines(f"{username}|{password}|{pwfalse}\n")
            writers.close()
            writers = open('self_info/result.txt', 'a+', encoding = "utf-8")
            writers.writelines(f"{username}|{password}|{pwfalse}\n")
            writers.close()
        driver.quit()
        return False
        
    driver.quit()

def main():
    username = open(r"username.txt", "r")
    reads = username.readlines()
    i = len(reads)
    for (read, length) in zip (reads, range(1, i)):
        akun = read.strip()
        username = akun.split("|")[0]
        password = akun.split("|")[1]
        info = open(r"self_info/success.txt", "r")
        success = info.readlines()
        insuccess = len(success)
        try:
            continued = timestamp(username, password, length, i, insuccess)
            if not continued:
                continue
        except:
            continued = timestamp(username, password, length, i, insuccess)
            if not continued:
                continue
            
if __name__ == '__main__':
    main()