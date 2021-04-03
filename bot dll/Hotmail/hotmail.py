from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector
import random
import json
import string
import gspread
from oauth2client.service_account import ServiceAccountCredentials
    
def get(user, i, length, nikname):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://signup.live.com/signup')
    driver.implicitly_wait(30)
    
    print("[ INFO ]__main__: In Progress "+ str(i) + "/" + str(length) )
    
    driver.find_elements_by_xpath('//*[@class="secondary-text"]')[2].click()
    driver.implicitly_wait(10)
    
    try:
        try:
            #Input UserHotmail
            userHotmail = driver.find_element_by_name('MemberName')
            userHotmail.send_keys(user)
            driver.implicitly_wait(10)
            #driver.find_element_by_xpath('//*[@class="phoneCountry col-xs-24"]').click()
            #driver.find_elements_by_xpath('//*[@class="phoneCountry col-xs-24"]/option')[0].click()
            userHotmail.send_keys(Keys.RETURN)
            driver.implicitly_wait(20)
        except:
            print('[ ERROR ]__main__: Failed')
            return False
          
        try:  
            #Input Password
            passHotmail = driver.find_element_by_name('Password')
            passHotmail.send_keys('Semogaberkah')
            passHotmail.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
        except:
            print('[ ERROR ]__main__: Failed')
        
        try:
            #Input FirstName && LastName
            fullName = nikname.split()
            firstName = fullName[0]
            lastName = fullName[1]

            first_name = driver.find_element_by_name('FirstName')
            first_name.send_keys(firstName)
            driver.implicitly_wait(10)
                    
            last_name = driver.find_element_by_name('LastName')
            last_name.send_keys(lastName)
                
            driver.implicitly_wait(10)
            last_name.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
        except:
            print('[ ERROR ]__main__: Failed Input Nikname')
            driver.quit()
            return False
            
        try:
            rangeMounth = random.randint(1, 12)
            driver.find_element_by_xpath('//*[@class="datepart0 form-control"]').click()
            sleep(0.5)
            driver.find_elements_by_xpath('//*[@class="datepart0 form-control"]/option')[rangeMounth].click()
            driver.implicitly_wait(10)
                
            rangeDate = random.randint(1, 29)
            driver.find_element_by_xpath('//*[@class="datepart1 form-control"]').click()
            sleep(0.5)
            driver.find_elements_by_xpath('//*[@class="datepart1 form-control"]/option')[rangeDate].click()
            driver.implicitly_wait(10)
            
            try:
                rangeYears = random.randint(20, 37)
                driver.find_element_by_xpath('//*[@class="datepart2 form-control"]').click()
                sleep(0.5)
                driver.find_elements_by_xpath('//*[@class="datepart2 form-control"]/option')[rangeYears].click()
                driver.implicitly_wait(10)
            except:
                pass
                
            driver.find_element_by_xpath('//*[@class="inline-block"]').click()

            verivyHuman = input("[ INPUT ]__main__: Verivy Human : 1. Repeat   2. RETURN   3. Restart Network")
            if(verivyHuman == 1):
                get(user, i, length)
            elif(verivyHuman == 2):
                return False
            elif(str(verivyHuman) == '3'):
                driver.get('http://192.168.1.1/')
                driver.implicitly_wait(10)

                username = driver.find_element_by_name('Username')
                username.send_keys('user')
                driver.implicitly_wait(10)

                password = driver.find_element_by_name('Password')
                password.send_keys('user')
                driver.implicitly_wait(10)

                password.send_keys(Keys.RETURN)
                driver.implicitly_wait(10)
                    
                input("[ INPUT ]__main__: Restarting Network")
                    
            driver.implicitly_wait(30)    
            nikname = driver.find_element_by_css_selector('.css-350').text
            driver.implicitly_wait(10)
            
            print("[ INFO ]__main__: Success Create User : " + nikname)
            writers = open('Create User.txt', 'a+', encoding="utf-8")
            writers.writelines(f"{nikname}|User Success|")
            writers.close()
        except:
            print('[ ERROR ]__main__: Failed')
        
        try:
            #Recovery Email
            driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1616124711&rver=7.3.6960.0&wp=SA_20MIN&wreply=https%3A%2F%2Faccount.live.com%2Fproofs%2FManage%3Fmkt%3Den-us%26uiflavor%3Dweb%26mpcxt%3DCATB%26ru%3Dhttps%253A%252F%252Flogin.live.com%252Flogin.srf%253Fid%253D38936%2526opid%253DC36B5AF339314CAB%2526opidt%253D1591860510%26ocxt%3DTFA%26id%3D38936%26uaid%3D95f2b83ab0034b0d812938ed66d4436d&lc=1033&id=38936&mkt=en-US&uaid=95f2b83ab0034b0d812938ed66d4436d')
            driver.implicitly_wait(10)
            
            emailPemulihan = driver.find_element_by_name('EmailAddress')
            #recoveryEmail = input("Recovery Email : ")
            readRecoveryEmail = open(r"recoveryEmail.txt", "r+")
            recoveryEmail = readRecoveryEmail.read()
            emailPemulihan.send_keys(recoveryEmail)
            emailPemulihan.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
                
            #Verivy Recovery Email
            OTP = input("[ INPUT ]__main__: Enter Code OTP : ")
            verivyRecovery = driver.find_element_by_name('iOttText')
            verivyRecovery.send_keys(OTP)
            verivyRecovery.send_keys(Keys.RETURN)
            
            try:
                driver.implicitly_wait(10)
                driver.find_element_by_xpath('//*[@class="table-cell text-left content"]')
            except:
                sleep(3)
                print('Failed to Input OTP')
            
            print("[ INFO ]__main__: Recovery Email Success!!")
            writers = open('Create User.txt', 'a+', encoding="utf-8")
            localtime = time.asctime(time.localtime(time.time())).split()
            mounth = localtime[1]
            date = localtime[2]
            year = localtime[4]
            clock = localtime[3]
            writers.writelines(f"{recoveryEmail}|{mounth}-{date}-{year} {clock}\n")
            writers.close()
            
            driver.get('https://outlook.live.com/mail/0/inbox')
            driver.implicitly_wait(20)
            
            try:
                try:
                    driver.find_element_by_xpath('//*[@class="ms-Button _1ThK9dT4toWCphxfLMD8kj XX4OfPJHEtyyE1ffjCPFp ms-Button--commandBar ms-CommandBarItem-link root-78"]')
                    mark_read = driver.find_element_by_xpath('//*[@class="ms-Button _1ThK9dT4toWCphxfLMD8kj XX4OfPJHEtyyE1ffjCPFp ms-Button--commandBar ms-CommandBarItem-link root-78"]')
                    mark_read.click()
                    driver.implicitly_wait(10)
                    
                    close = driver.find_element_by_xpath('//*[@class="ms-Button ms-Button--icon _2Hr138oc3hd2OQdmKNYj3W root-58"]')
                    close.click()
                    driver.implicitly_wait(10)
                except:
                    driver.find_element_by_xpath('//*[@class="ms-Button _1ThK9dT4toWCphxfLMD8kj XX4OfPJHEtyyE1ffjCPFp ms-Button--commandBar ms-CommandBarItem-link root-79"]').click()
                    driver.find_element_by_xpath('//*[@class="ms-Button ms-Button--icon _2Hr138oc3hd2OQdmKNYj3W root-59"]').click()
                    
                setting = driver.find_elements_by_xpath('//*[@class="_2-4jfRBkDLE1Xuu-op_VA2 o365sx-button"]')[2]
                setting.click()
                driver.implicitly_wait(10)
                sleep(2)
                
                theme = random.randint(1, 9)
                choseTema = driver.find_elements_by_xpath('//*[@class="_2NkmWEH68hmtsoAMpmU6Rk"]')[theme].click()
                driver.implicitly_wait(10)
                    
                hide = driver.find_elements_by_xpath('//*[@class="ms-ChoiceField-wrapper"]')[5].click()
                #driver.execute_script("return arguments[0].scrollIntoView();", hide)
                driver.implicitly_wait(10)

                print("[ INFO ]__main__: Setting Succes")
            except:
                setting = driver.find_elements_by_xpath('//*[@class="_2-4jfRBkDLE1Xuu-op_VA2 o365sx-button"]')[2]
                setting.click()
                driver.implicitly_wait(10)
                sleep(2)
                
                theme = random.randint(1, 9)
                choseTema = driver.find_elements_by_xpath('//*[@class="_2NkmWEH68hmtsoAMpmU6Rk"]')[theme].click()
                driver.implicitly_wait(10)
                    
                hide = driver.find_elements_by_xpath('//*[@class="ms-ChoiceField-wrapper"]')[5].click()
                #driver.execute_script("return arguments[0].scrollIntoView();", hide)
                driver.implicitly_wait(10)

                print("[ INFO ]__main__: Setting Succes")
            
            for multiples in range(3,length,3):
                if(i == multiples):
                    driver.get('http://192.168.1.1/')
                    driver.implicitly_wait(10)

                    username = driver.find_element_by_name('Username')
                    username.send_keys('user')
                    driver.implicitly_wait(10)

                    password = driver.find_element_by_name('Password')
                    password.send_keys('user')
                    driver.implicitly_wait(10)

                    password.send_keys(Keys.RETURN)
                    driver.implicitly_wait(10)
                    
                    input("[ INPUT ]__main__: Restarting Network")
                    
            messages = input("[ INPUT ]__main__: Press Enter To Continued!!  Or Input n To Restart Network!! ")
            if(messages == 'n'):
                driver.get('http://192.168.1.1/')
                driver.implicitly_wait(10)

                username = driver.find_element_by_name('Username')
                username.send_keys('user')
                driver.implicitly_wait(10)

                password = driver.find_element_by_name('Password')
                password.send_keys('user')
                password.send_keys(Keys.RETURN)
                driver.implicitly_wait(10)
                try:
                    administrator = driver.find_element_by_css_selector('.h2_s').click()
                except:
                    print('Failed Parse Administrator')
                    
        except:
            print('[ ERROR ]__main__: Failed')
            #Recovery Again
            driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1616124711&rver=7.3.6960.0&wp=SA_20MIN&wreply=https%3A%2F%2Faccount.live.com%2Fproofs%2FManage%3Fmkt%3Den-us%26uiflavor%3Dweb%26mpcxt%3DCATB%26ru%3Dhttps%253A%252F%252Flogin.live.com%252Flogin.srf%253Fid%253D38936%2526opid%253DC36B5AF339314CAB%2526opidt%253D1591860510%26ocxt%3DTFA%26id%3D38936%26uaid%3D95f2b83ab0034b0d812938ed66d4436d&lc=1033&id=38936&mkt=en-US&uaid=95f2b83ab0034b0d812938ed66d4436d')
            driver.implicitly_wait(10)
            
            emailPemulihan = driver.find_element_by_name('EmailAddress')
            recoveryEmail = input("[ INPUT ]__main__: Recovery Email : ")
            emailPemulihan.send_keys(recoveryEmail)
            driver.implicitly_wait(10)
            emailPemulihan.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
                
            #Verivy Recovery Email
            OTP = input("[ INPUT ]__main__: Enter Code OTP : ")
            verivyRecovery = driver.find_element_by_name('iOttText')
            verivyRecovery.send_keys(OTP)
            verivyRecovery.send_keys(Keys.RETURN)
            driver.implicitly_wait(10)
            
            try:
                driver.implicitly_wait(10)
                driver.find_element_by_xpath('//*[@class="table-cell text-left content"]')
            except:
                sleep(3)
                print('Failed to Input OTP')
                
            print("[ INFO ]__main__: Recovery Email Success!!")
            writers = open('Create User.txt', 'a+', encoding="utf-8")
            localtime = time.asctime(time.localtime(time.time())).split()
            mounth = localtime[1]
            date = localtime[2]
            year = localtime[4]
            clock = localtime[3]
            writers.writelines(f"{recoveryEmail}|{mounth}-{date}-{year} {clock}\n")
            writers.close()
            
            driver.get('https://outlook.live.com/mail/0/inbox')
            driver.implicitly_wait(20)
            
            try:
                driver.find_element_by_xpath('//*[@class="ms-Button _1ThK9dT4toWCphxfLMD8kj XX4OfPJHEtyyE1ffjCPFp ms-Button--commandBar ms-CommandBarItem-link root-78"]')
                mark_read = driver.find_element_by_xpath('//*[@class="ms-Button _1ThK9dT4toWCphxfLMD8kj XX4OfPJHEtyyE1ffjCPFp ms-Button--commandBar ms-CommandBarItem-link root-78"]')
                mark_read.click()
                driver.implicitly_wait(10)
                
                close = driver.find_element_by_xpath('//*[@class="ms-Button ms-Button--icon _2Hr138oc3hd2OQdmKNYj3W root-58"]')
                close.click()
                driver.implicitly_wait(10)
                    
                setting = driver.find_elements_by_xpath('//*[@class="_2-4jfRBkDLE1Xuu-op_VA2 o365sx-button"]')[2]
                setting.click()
                driver.implicitly_wait(10)
                sleep(2)
                
                theme = random.randint(0, 9)
                choseTema = driver.find_elements_by_xpath('//*[@class="_2NkmWEH68hmtsoAMpmU6Rk"]')[theme].click()
                driver.implicitly_wait(10)
                    
                hide = driver.find_elements_by_xpath('//*[@class="ms-ChoiceField-wrapper"]')[5].click()
                #driver.execute_script("return arguments[0].scrollIntoView();", hide)
                driver.implicitly_wait(10)
            except:
                pass
    except:
        print("[ INFO ]__main__: Failed to Create New User!!")
        writers = open('Create User.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{user}|Failed\n")
        writers.close()
        
    driver.quit()
    
def createUserHotmail():
    user = open(r"username.txt", "r+")
    reads = user.readlines()
    length = len(reads)
    
    for (read, i) in zip (reads, range(1, length)):
        nikname = read.strip()
        resultsUser = nikname.replace(" ", "")
        randomInt = random.randint(1, 99)
        letters = string.ascii_lowercase
        data = ''.join(random.choice(letters) for i in range(2))
        sliceUser = resultsUser[0:7].lower()
        user = sliceUser + str(randomInt)
        continued = get(user, i, length, nikname)
        if not continued:
            continue
    
if __name__ == '__main__':
    try:
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
    except:
        print('Login Failed!! error connection!!')
        sleep(3)
        
    user = open(r"data/config.json", "r")
    dataJsons = json.load(user)
    emailConfig = dataJsons['lisensi']['email']
    passwordConfig = dataJsons['lisensi']['pwd']
    userAgentConfig = dataJsons['lisensi']['user-agent']
        
    if email == emailConfig and password == passwordConfig and userAgent == userAgentConfig and status == 'Active':
        createUserHotmail()
    elif status != 'Active':
        print('Login Failed!! Your Config non-active')
        sleep(3)
    else:
        print('Login Failed!! Check your config')
        sleep(3)
    
    