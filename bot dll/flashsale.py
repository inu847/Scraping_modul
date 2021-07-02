from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from parsel import Selector
import datetime


driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(20)
# driver.minimize_window()
driver.get('https://shopee.co.id/buyer/login')
driver.implicitly_wait(20)

user = driver.find_element_by_name('loginKey')
user.send_keys('afridaazha5')
passwd = driver.find_element_by_name('password')
passwd.send_keys('Semogaberkah')
    
passwd.send_keys(Keys.RETURN)
driver.implicitly_wait(20)

try:
    driver.find_element_by_xpath('//*[@class="_3fBm1wELGG"]')
    print(username + ' success logon')
except:
    print('Gagal Login cek username password')
    driver.quit()

input()
x = datetime.datetime.now()

time = input("Masukkan Deadline (08:12)")
y = time.split(":")

hI = int(y[0])
mI = int(y[1])

h = int(x.strftime("%H"))
m = int(x.strftime("%M"))

if h >= hI and m >= mI:
	print(str(h)+":"+str(m))
else:
	print(x.strftime("%H:%M"))