from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('http://127.0.0.1:4000/tapahtumat.html')
time.sleep(2)

logs = driver.get_log('browser')
for log in logs:
    print(log)

driver.quit()
