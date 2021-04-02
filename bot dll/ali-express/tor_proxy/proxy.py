from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

PROXY = "socks5://127.0.0.1:9050"
chrome_options = Options()
#chrome_options.add_argument("--HTTPTunnelPort socks5://127.0.0.1:9050")
chrome_options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get("https://www.aliexpress.com/af/category/1509.html?categoryBrowse=y&origin=n&CatId=1509&spm=a2g0o.best.106.1.40232c25IfwHXe&catName=jewelry-accessories")