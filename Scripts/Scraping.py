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
import os
from FetchProperties import FetchProperties

""" Setting Basic Logging Options """

if not os.path.exists('../Logs') :
    os.makedirs('../Logs')

LOG_FILENAME = datetime.now().strftime('../Logs/scraping_app_%d_%m_%Y.log')
logging.basicConfig(filename=LOG_FILENAME, filemode='a', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)

""" Fetching Configuration From Properties File """

fetchProperties = FetchProperties()
configuration = fetchProperties.main()

""" Initializing Data From Properties file to Execute Web Scraping """

url = configuration.get("url").data
browser = webdriver.Chrome()
browser.get(url)

browser.find_element(By.LINK_TEXT, configuration.get("province").data).click()
browser.find_element(By.LINK_TEXT, configuration.get("area").data).click()

browser.find_element_by_id("LocUpdate").click()

time.sleep(2)
browser.find_element_by_id("SearchKeyword").send_keys(configuration.get("keyword").data)
browser.find_element_by_name("SearchSubmit").click()

time.sleep(20)
browser.find_element_by_xpath("/html/body/div[3]/div[3]/div[3]/div[2]/div[1]/div/ul[3]/ul/li[2]/a").click()

""" Reached Advertisement Page To Begin Data Scraping """
time.sleep(20)
advertisements = browser.find_elements_by_class_name("regular-ad")
print(len(advertisements))

ad_Links = []

for ads in advertisements :
    ad_Links.append(ads.find_element_by_tag_name("a").get_attribute('href'))
    print(ads.find_element_by_tag_name("a").get_attribute('href'))

for link in ad_Links :
    browser.get(link)

print(len(ad_Links))
