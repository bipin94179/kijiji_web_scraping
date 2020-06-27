import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
from bs4 import BeautifulSoup
import re

""" Setting Basic Logging Options """
LOG_FILENAME = datetime.now().strftime('../Logs/scraping_app_%d_%m_%Y.log')
logging.basicConfig(filename=LOG_FILENAME, filemode='a', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)


""" Download the ChromDriver in the /usr/local/bin """
""" Run the following command to give all the rights to the executable : xattr -d com.apple.quarantine chromedriver """

url = "https://www.kijiji.ca"
driver = webdriver.Chrome()
driver.get(url)

driver.find_element(By.LINK_TEXT, "Alberta").click()
driver.find_element(By.LINK_TEXT, "Calgary").click()

driver.find_element_by_id("LocUpdate").click()

""" WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "SearchSubmit"))) """
time.sleep(2)
driver.find_element_by_id("SearchKeyword").send_keys("Office Space")
driver.find_element_by_name("SearchSubmit").click()

url_scrap = driver.current_url

response = requests.get(url_scrap)

soup = BeautifulSoup(response.text, 'html.parser')

post = soup.find_all('a', {'href': re.compile(
    r'["/-a-zA-Z0-9]*')}, {'class_': re.compile(r'title')})

# post = soup.find_all(re.compile("^a.href"))

fi = open('file.txt', 'w')

for tag in post:
    fi.write(str(tag.get_text()))

fi.close()


# title_list = []
# for item in post:
#     title = item.get_text()
#     title_list.append(title.strip())

# print(title_list)
