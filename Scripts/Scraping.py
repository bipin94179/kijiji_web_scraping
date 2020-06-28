import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests
import re
import os
from FetchProperties import FetchProperties
from Extract import Extract

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
wait = WebDriverWait(browser, 10)
browser.get(url)
browser.maximize_window()

""" Updating Location """

time.sleep(10)

province = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, configuration.get("province").data)))
province.click()

area = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, configuration.get("area").data)))
area.click()

location_update = wait.until(EC.element_to_be_clickable((By.ID, 'LocUpdate')))
location_update.click()

""" Searching Keywords """

time.sleep(10)

search_box = wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
search_box.send_keys(configuration.get("keyword").data)

search_button = wait.until(EC.element_to_be_clickable((By.NAME, 'SearchSubmit')))
search_button.click()

""" Get Wanted Advertisements """

attribute_selected_elements = browser.find_elements_by_tag_name("a")
for selected_elements in attribute_selected_elements :
    if selected_elements.get_attribute('data-event') == "wantedSelection" :
        wanted_link = selected_elements.get_attribute('href')
        browser.get(wanted_link)
        break

""" Fetching Total No Of Pages """

showing = browser.find_element_by_class_name("showing")
showing_text = showing.text
total_advertisements = showing_text.split(' ')[5]
current_advertisements = showing_text.split(' ')[3]
total_pages = int(total_advertisements)/int(current_advertisements)
print(showing_text)
print(total_advertisements)
print(current_advertisements)
print(total_pages)

""" Fetching Advertisement Links """

advertisment_links = []
advertisements = browser.find_elements_by_class_name("regular-ad")
for ad in advertisements :
    advertisment_links.append(ad.find_element_by_tag_name("a").get_attribute('href'))