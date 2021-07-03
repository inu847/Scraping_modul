from discord_webhook import DiscordWebhook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests
from time import gmtime, strftime, sleep
from random import randint
import subprocess
import pathlib
import ctypes
import os
import datetime

dateTimeObj = datetime.datetime.now()
timestampStr = dateTimeObj.strftime("%H:%M:%S")

def newtime():
	global dateTimeObj
	global timestampStr
	dateTimeObj = datetime.datetime.now()
	timestampStr = dateTimeObj.strftime("%H:%M:%S")

def main():
    webhook = 0
    response = 0

    # STARTUP EVENT

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Flashsale Sniper [Platform : Shopee Edition Flash Sale]")
    producturl = input("Masukkan URL Product: ")
    flash_sale = input("Masukkan Jadwal Flash Sale *format(jam:menit) : ")
    username = input("Masukkan Username Shopee: ")
    password = input("Masukkan Password Shopee: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    print("Flashsale Sniper [Platform : Shopee Edition Flash Sale]")
    print("");
    print("Mohon masukkan metode pembayaran yang ingin dipakai")
    print("[1] : ShopeePay (Pastikan Saldo Cukup)")
    print("[2] : Bank BCA (Cek Otomatis)")
    print("[3] : Bank Mandiri (Cek Otomatis)")
    print("[4] : Bank BNI (Cek Otomatis)")
    print("[5] : Bank BRI (Cek Otomatis)")
    print("[6] : Bank Syariah Mandiri (Cek Otomatis)")
    print("[7] : Bank Permata (Dicek Otomatis)")
    
    pembayaran = int(input("Pilihan metode pembayaran (1-6) > "))
    pakelog = input("Apakah anda ingin memantau aktivitas Sniping via Discord? (y/n) > ")
    if pakelog == "y":
        print("Masukkan URL Webhook Discord untuk Aktivitas Pemantauan")
        logs = input("Webhook URL > ")
        # PREPARATION EVENT
        print("Pemantauan sniping telah diaktifkan.")
        sleep(2)
    else:
        logs = "fuck off lol"
        print("Pemantauan sniping telah dinonaktifkan.")
        sleep(2)

    os.system('cls' if os.name == 'nt' else 'clear')

    print("Flashsale Sniper [Platform : Shopee Edition]")
    print("")
    print("The date and time now is",strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    print("Please ensure you're using the best quality proxy possible!.")
    print("")
    print("Awaiting for the time to manual prevent bot detection...");

    # MAIN EVENTS

    # LOGGING IN TO THE ACCOUNT

    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ['enable-automation']);
    #option.add_argument("--headless")
    browser = webdriver.Chrome(options=option)
    browser.get("https://shopee.co.id/buyer/login")
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/form/div/div[2]/button"))
        )
    finally:
        newtime()
    print("[",timestampStr,"]""[INFO :] SNIPING START!")
    dateTimeObj = datetime.datetime.now()
    print("[",timestampStr,"]""[INFO :] LOGGING INTO ACCOUNT")
    user = browser.find_element_by_name('loginKey')
    user.send_keys(username)
    passwd = browser.find_element_by_name('password')
    passwd.send_keys(password)
        
    passwd.send_keys(Keys.RETURN)
    sleep(5)

    # START SNIPING

    newtime()
    print("[",timestampStr,"]""[INFO :] LOGIN ACTIVITY DONE, NOW SNIPING...")
    webhook = DiscordWebhook(url=logs, content='[INFO :] LOGIN ACTIVITY DONE, NOW SNIPING...')
    if pakelog == "y":
        response = webhook.execute()
    newtime()
    print("[",timestampStr,"]""[INFO :] REDIRECTING INTO THE SPECIFIED PRODUCT URL...")
    webhook = DiscordWebhook(url=logs, content='[INFO :] REDIRECTING INTO THE SPECIFIED PRODUCT URL...')
    if pakelog == "y":
        response = webhook.execute()

    browser.get(producturl)

    newtime()
    print("[",timestampStr,"]""[INFO :] CHECKING IF PRODUCT VARIANT EXISTS...")
    webhook = DiscordWebhook(url=logs, content='[INFO :] CHECKING IF PRODUCT VARIANT EXISTS...')
    hasvariant = 1
    if pakelog == "y":
        response = webhook.execute()

    try:
        element = WebDriverWait(browser, 1).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='product-variation']"))
        )

    except TimeoutException:
        newtime()
        print("[",timestampStr,"]""[INFO :] NO PRODUCT VARIANT FOUND, CONTINUING SNIPING PROCESS...")
        webhook = DiscordWebhook(url=logs, content='[INFO :] NO PRODUCT VARIANT FOUND, CONTINUING SNIPING PROCESS...')
        hasvariant = 0
        if pakelog == "y":
            response = webhook.execute()

    if hasvariant == 1:
        productvariant = browser.find_elements_by_xpath("//*[@class='product-variation']")
        listVarian = [data.text for data in productvariant]
        for (varian, i) in zip(listVarian, range(0, len(listVarian)+1)):
            print('['+str(i)+']. '+varian)
        
        newtime()
        print("[",timestampStr,"]""[INFO :] VARIANT PRODUK DITEMUKAN, SILAHKAN KETIK NOMOR LIST VARIANT")
        webhook = DiscordWebhook(url=logs, content='[INFO :] VARIANT PRODUK DITEMUKAN, SILAHKAN KETIK NOMOR LIST VARIANT DI CONSOLE')
        if pakelog == "y":
            response = webhook.execute()
        inputvariant = int(input("Masukkan nomor variant product >"))

    while True:
        try:
            element = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "//*[text()='beli sekarang']")))
            belisekarang = browser.find_element_by_xpath("//*[text()='beli sekarang']")
            newtime()
            print("[",timestampStr,"]""[INFO :] ORDER BUTTON FOUND, ATTEMPTING TO SUBMIT...")
            webhook = DiscordWebhook(url=logs, content='[INFO :] ORDER BUTTON FOUND, ATTEMPTING TO SUBMIT...')
            if pakelog == "y":
                response = webhook.execute()
            break
        except NoSuchElementException:
            newtime()
            print("[",timestampStr,"]""[INFO :] ORDER BUTTON NOT FOUND, REFRESHING THE PAGE...")
            webhook = DiscordWebhook(url=logs, content='[INFO :] ORDER BUTTON NOT FOUND, REFRESHING THE PAGE...')
            if pakelog == "y":
                response = webhook.execute()
            browser.refresh()
            continue
        except TimeoutException:
            newtime()
            print("[",timestampStr,"]""[INFO :] ORDER BUTTON NOT FOUND, REFRESHING THE PAGE...")
            webhook = DiscordWebhook(url=logs, content='[INFO :] ORDER BUTTON NOT FOUND, REFRESHING THE PAGE...')
            if pakelog == "y":
                response = webhook.execute()
            browser.refresh()
            continue
    print(belisekarang.is_enabled())
    btnclass = belisekarang.get_attribute("class")
    print(btnclass)

    while True:
        if 'disabled' in btnclass:
            newtime()
            webhook = DiscordWebhook(url=logs, content='[INFO :] ORDER BUTTON DISABLED, REFRESHING THE PAGE...')
            if pakelog == "y":
                response = webhook.execute()
            print("[",timestampStr,"]""[INFO :] ORDER BUTTON DISABLED!, REFRESHING THE PAGE...")
            browser.refresh()
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[5]/div/div/button[2]")))
            belisekarang = browser.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[5]/div/div/button[2]")
            btnclass = belisekarang.get_attribute("class")
        else:
            if hasvariant == 1:
                try:
                    productvariant[inputvariant].click()
                except:
                    while True:
                        print('[ ERROR ] Variasi Tidak tersedia')
                        inputvariant = int(input("Masukkan nomor variant product >"))
                        try:
                            productvariant[inputvariant].click()
                            break
                        except:
                            pass

            belisekarang.click()
            newtime()
            webhook = DiscordWebhook(url=logs, content='[INFO :] ORDER BUTTON ENABLED, ATTEMPTING TO PUT ITEM IN CART...')
            if pakelog == "y":
                response = webhook.execute()
            print("[",timestampStr,"]""[INFO :] ORDER BUTTON ENABLED!, ATTEMPTING TO PUT ITEM IN CART...")
            break
        
    checkout(browser, pembayaran, logs, pakelog, flash_sale)
    # try:
    # except:
    #     while True:
    #         try:
    #             print("Mohon masukkan metode pembayaran yang ingin dipakai")
    #             print("[1] : ShopeePay (Pastikan Saldo Cukup)")
    #             print("[2] : Bank BCA (Cek Otomatis)")
    #             print("[3] : Bank Mandiri (Cek Otomatis)")
    #             print("[4] : Bank BNI (Cek Otomatis)")
    #             print("[5] : Bank BRI (Cek Otomatis)")
    #             print("[6] : Bank Syariah Mandiri (Cek Otomatis)")
    #             print("[7] : Bank Permata (Dicek Otomatis)")
    #             pembayaran = int(input("Pilihan ulang metode pembayaran (1-6) > "))
    #             checkout(browser, pembayaran, logs, pakelog)
    #             break
    #         except:
    #             pass

def checkout(browser, pembayaran, logs, pakelog, flash_sale):
    newtime()
    print("[",timestampStr,"]""[INFO :] SUCCESSFULLY PUT ITEM INTO CART!")
    webhook = DiscordWebhook(url=logs, content='[INFO :] SUCCESSFULLY PUT ITEM INTO CART!')
    if pakelog == "y":
        response = webhook.execute()

    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[text()='checkout']"))
        )
    finally:
        checkout = browser.find_element_by_xpath("//*[text()='checkout']")
        
    # START CHECKOUT PR
    newtime()
    print("[",timestampStr,"]""[INFO :] ATTEMPTING TO CHECKOUT ITEM.")
    browser.execute_script("arguments[0].click();", checkout)
    # checkout.click()
    webhook = DiscordWebhook(url=logs, content='[INFO :] ATTEMPTING TO CHECKOUT ITEM.')
    if pakelog == "y":
        response = webhook.execute()

    browser.implicitly_wait(10)
    ubahOngkir = browser.find_element_by_xpath('//*[@class="_26DEZ8"]')
    browser.execute_script("arguments[0].click();", ubahOngkir)
    sleep(2)
    browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//*[text()="Pengiriman setiap saat"]'))
    sleep(2)
    browser.execute_script("arguments[0].click();", browser.find_element_by_xpath('//*[@class="stardust-button stardust-button--primary -T3OGq"]'))

    bankmethod = ""
    try:
        browser.implicitly_wait(10)
        bankmethod = browser.find_element_by_xpath("//*[text()='Transfer Bank']")
    except:
        print("not found!!")
    
    # ShopeePay
    if pembayaran == 1:
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='ShopeePay']"))
            )
            shopeepay =  browser.find_element_by_xpath("//*[text()='ShopeePay']")
            browser.execute_script("arguments[0].click();", shopeepay)
        except:
            print('Saldo Anda Tidak Mencukupi!!\n')
        
    # Bank BCA (Cek Otomatis)
    elif pembayaran == 2:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text()='Bank BCA (Dicek Otomatis)']"))
            )
        finally:
            bankbca = browser.find_element_by_xpath("//*[text()='Bank BCA (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK BCA AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING BANK BCA AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        bankbca.click()

    # Bank Mandiri (Cek Otomatis)
    elif pembayaran == 3:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text='Bank Mandiri & Bank Lainnya (Dicek Otomatis)']"))
            )
        finally:
            mandiri1 = browser.find_element_by_xpath("//*[text='Bank Mandiri & Bank Lainnya (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK MANDIRI AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING BANK MANDIRI AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        mandiri1.click()

    # Bank BNI (Cek Otomatis)
    elif pembayaran == 4:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text='Bank BNI (Dicek Otomatis)']"))
            )
        finally:
            bankbni = browser.find_element_by_xpath("//*[text='Bank BNI (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK BNI AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING BANK BNI AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        bankbni.click()

    # Bank BRI (Cek Otomatis)
    elif pembayaran == 5:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text='Bank BRI (Dicek Otomatis)']"))
            )
        finally:
            bankbri = browser.find_element_by_xpath("//*[text='Bank BRI (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK BRI AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING BANK BRI AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        bankbri.click()

    # Bank Syariah Mandiri (Cek Otomatis)
    elif pembayaran == 6:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text='Bank Syariah Indonesia (BSI) (Dicek Otomatis)']"))
            )
        finally:
            mandirisyariah = browser.find_element_by_xpath("//*[text='Bank Syariah Indonesia (BSI) (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING MANDIRI SYARI'AH AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING MANDIRI SYARIAH AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        mandirisyariah.click()
    
    # Bank Permata (Dicek Otomatis)
    elif pembayaran == 7:
        browser.execute_script("arguments[0].click();", bankmethod)
        sleep(2)
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING BANK AS PAYMENT METHOD.")
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[text='Bank Permata (Dicek Otomatis)']"))
            )
        finally:
            mandirisyariah = browser.find_element_by_xpath("//*[text='Bank Permata (Dicek Otomatis)']")
        newtime()
        print("[",timestampStr,"]""[INFO :] SELECTING MANDIRI SYARI'AH AS THE BANK.")
        webhook = DiscordWebhook(url=logs, content='[INFO :] SELECTING MANDIRI SYARIAH AS THE BANK.')
        if pakelog == "y":
            response = webhook.execute()
        mandirisyariah.click()

    else:
        print("Invalid payment method specified!, please try again later.")
        print("Sniping failed!")

    times_flashSale = flash_sale.split(":")
    hI = int(times_flashSale[0])
    mI = int(times_flashSale[1])
    # WAIT STORE
    while True:
        x = datetime.datetime.now()
        h = int(x.strftime("%H"))
        m = int(x.strftime("%M"))
        s = int(x.strftime("%S"))
        rate_hourse = hI - h
        rate_minuite = mI - m
        rate_second = 0 - s
        hourse_second = rate_hourse*3600
        minute_second = rate_minuite*60
        
        limit = hourse_second + minute_second + rate_second
        sleep(0.1)
        os.system('cls')
        print("[",timestampStr,"]""[INFO :] "+str(limit)+ " second")
        print()
        if limit <= 0:
            print("finished!!")
            break

    # BUAT ORDER
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stardust-button"))
        )
    finally:
        newtime()
        print("[",timestampStr,"]""[INFO :] CREATING YOUR ORDER.")
    webhook = DiscordWebhook(url=logs, content='[INFO :] CREATING YOUR ORDER.')
    if pakelog == "y":
        response = webhook.execute()
    makeorder = browser.find_element_by_class_name("stardust-button")
    browser.execute_script("arguments[0].click();", makeorder)
    # makeorder.click()

    # END EVENT
    newtime()
    print("[",timestampStr,"]""[INFO :] SUCCESSFULLY ATTEMPTED TO SNIPE PRODUCT!")
    webhook = DiscordWebhook(url=logs, content='[INFO :] SUCCESSFULLY ATTEMPTED TO SNIPE PRODUCT!')
    if pakelog == "y":
        response = webhook.execute()
    newtime()
    print("[",timestampStr,"]""[INFO :] PLEASE CHECK YOUR ORDER LIST ON UNPAID!.")
    webhook = DiscordWebhook(url=logs, content='[INFO :] PLEASE CHECK YOUR ORDER LIST ON UNPAID!')
    if pakelog == "y":
        response = webhook.execute()
    print("Your request product has been sniped at",strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    sleep(2)
    webhook = DiscordWebhook(url=logs, content='Your request product has been successfully sniped!')
    if pakelog == "y":
        response = webhook.execute()
    print("We will close our script by 10 seconds.")
    webhook = DiscordWebhook(url=logs, content='The console will close at few seconds.')
    if pakelog == "y":
        response = webhook.execute()
    sleep(10)
    
if __name__ == '__main__':
    main()