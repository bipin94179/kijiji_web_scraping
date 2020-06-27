import logging
from datetime import datetime
from SetupEnvironment import SetupEnvironment
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
from bs4 import BeautifulSoup

""" Setting Basic Logging Options """
LOG_FILENAME = datetime.now().strftime('../Logs/scraping_app_%d_%m_%Y.log')
logging.basicConfig(filename=LOG_FILENAME, filemode='a', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)


""" Download the ChromDriver in the /usr/local/bin """
""" Run the following command to give all the rights to the executable : xattr -d com.apple.quarantine chromedriver """

""" Going to the Main Website URL  """

url = "https://www.kijiji.ca"
browser = webdriver.Chrome()
browser.get(url)

""" Selecting a Particular Location And Area """

browser.find_element(By.LINK_TEXT,"Alberta").click()
browser.find_element(By.LINK_TEXT,"Calgary").click()

browser.find_element_by_id("LocUpdate").click()

time.sleep(2)

""" Searching a Particular Keyword """

browser.find_element_by_id("SearchKeyword").send_keys("Office Space")
browser.find_element_by_name("SearchSubmit").click()

url_scrap = browser.current_url
response = requests.get(url_scrap)
print(response)

""" soup = BeautifulSoup(response.text, 'html.parser')

post = soup.find_all(class_='title')

title_list=[]
for item in post:
    title = item.get_text()
    title_list.append(title.strip())

print(title_list) """

browser.quit()