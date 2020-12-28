from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.maximize_window()
driver.get('https://seller.shopee.co.id/portal/product/list/all')
driver.implicitly_wait(20)

user = driver.find_element_by_xpath('//*[@autocomplete="username"]')
user.send_keys('inu_ganteng')

driver.implicitly_wait(20)

passwd = driver.find_element_by_xpath('//*[@autocomplete="current-password"]')
passwd.send_keys('Komputer007')
driver.implicitly_wait(20)

driver.find_element_by_xpath('//*[@class="shopee-button shopee-button--primary shopee-button--large shopee-button--block"]').click()




# import mysql.connector

# mydb = mysql.connector.connect(host="localhost",
#                                user="root",
#                                password="",
#                                database="test")

# if mydb.is_connected:
#   print('Koneksi berhasil')

#   sql = "insert into learn(message, add=) values (%s, %s, %s)"

#   mycursor = mydb.cursor()
#   data = ('John', 'hallo')
#   mycursor.execute(sql, data)
#   mydb.commit()
#   print(mycursor.rowcount, "record inserted.")