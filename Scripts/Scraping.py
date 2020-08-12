""" This is the Starting Point of Kijiji Web Scraping Script """

from Logging import Logging
from HandleProperties import HandleProperties
import pathlib

from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from Extract import Extract
import math
from selenium.webdriver.chrome.options import Options  
import sys
import json
from oslo_concurrency import lockutils
from oslo_concurrency import processutils

""" Getting Basic Logging Options """

logger = Logging().get_logger("scraping")

""" Fetching Configuration From Properties File """

scraping_script_path = pathlib.Path(__file__).parent.absolute()
handleProperties = HandleProperties()
configuration = handleProperties.read_properties(str(scraping_script_path) + "/Config/Scraping.properties")

""" Initializing Variables """

advertisment_links = set()

total_command_line_arguments = len(sys.argv)
logger.debug("Length of Arguments : " + str(total_command_line_arguments))
if total_command_line_arguments > 5 or total_command_line_arguments < 5:
    logger.debug("Scraping Module : Incorrect No Of Arguments Passed")
    logger.debug("Scraping Module : System exiting")
    sys.exit()

province_argument = sys.argv[1]
city_argument = sys.argv[2]
type_argument = sys.argv[3]
search_keywords = sys.argv[4]

""" Initializing Data From Properties file to Execute Web Scraping """

file_path = str(scraping_script_path) + "/Scripts/Location.json"

@lockutils.synchronized('not_thread_process_safe', external=True, fair=True, lock_path=str(scraping_script_path) + "/Lock/")
def openFile (openMode, location_dictionary) :
    if openMode == "r" :
        with open(file_path, openMode, encoding='utf-8') as jsonFile:
            return json.load(jsonFile)
    if openMode == "w" :
        with open(file_path, openMode, encoding='utf-8') as jsonFile:
            json.dump(location_dictionary ,jsonFile)


location_dictionary = openFile("r", "")
province_dictionary = location_dictionary["province_dict"]
city_dictionary = location_dictionary["city_dict"]
province_name = province_dictionary.get(province_argument)
cities_json = city_dictionary.get(province_argument)
city_json = cities_json.get(city_argument)
city_name = city_json.get("name")

if type_argument == "w" :
    search_type = "Wanted"
    wanted_json = city_json.get("wanted")
    date_in_property = wanted_json["searchDate"]
    finalTimestamp_in_property = wanted_json.get("finalTimestamp")
elif type_argument == "o" :
    search_type = "Offering"
    offering_json = city_json.get("offering")
    date_in_property = offering_json["searchDate"]
    finalTimestamp_in_property = offering_json.get("finalTimestamp")

logger.debug("Province is : " + str(province_dictionary))
logger.info("Province Name is : " + str(province_name))
logger.debug("City is : " + str(city_json))
logger.debug("Cities are : " + str(cities_json))
logger.info("City Name is : " + str(city_name))
logger.info("Date from which Search Will Start : " + date_in_property)
logger.info("Timestamp from which Search Will Start : " + finalTimestamp_in_property)

# Getting Site Url from Property Configuration
site_url = configuration.get("url").data
logger.debug("Scraping Module : Initiating Scraping for : " + str(site_url))

# Initializing Chrome Web Driver and its Configuration

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument('window-size=1920x1080')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(options=chrome_options)

logger.debug("Scraping Module : Opening Chrome To Start Data Scraping")
# browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.refresh()
browser.delete_all_cookies()
browser.refresh()
browser.get(site_url)
browser.maximize_window()

""" Using Configuration Properties for Site Actions """

# Getting Selenium Element for Province and Clicking on it
# province_name = configuration.get("province").data
logger.debug("Scraping Module : Scraping Data For Province : " + str(province_name))
province = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, province_name)))
province.click()

# Getting Selenium Element for City and Clicking on it
# city_name = configuration.get("city").data
logger.debug("Scraping Module : Scraping Data For City : " + str(city_name))
city = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, city_name)))
city.click()

# Getiing Selenium Element For Submitting Location and Clicking on it
location_update = wait.until(EC.element_to_be_clickable((By.ID, 'LocUpdate')))
location_update.click()

language_update = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'headerLinkLanguage-203031519')))
if language_update.get_attribute('title') == 'English' :
    language_update.click()

# Splitting Search Keywords To Intitiate Searching
keywords = search_keywords.split(',')
logger.debug("Scraping Module : Searching Keywords Are : " + str(keywords))

# Search Started Using For Each Loop
for keyword in keywords :

    logger.debug("Scraping Module : Initiating Search For Keyword : " + str(keyword.strip()))

    # Getting Selenium Element for Search Input Box And Entering the Search Keyword
    search_box = wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
    search_box.send_keys(keyword.strip())
    
    # Getting Selenium Element for Search Submit Button And Clicking on it
    search_button = wait.until(EC.element_to_be_clickable((By.NAME, 'SearchSubmit')))
    search_button.click()

    # Waiting for Page to Load
    logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
    time.sleep(10)

    """ Get Wanted Advertisements """

    search_type_link = ''
    real_estate_link = ''
    for_rent_link = ''
    office_link = ''
    proceed_with_scraping = True

    # This Method is used to Extract Specific Link from Anchor Tag Selenium Elements
    def extract_link (data_event, link_type) :
        attribute_selected_elements = browser.find_elements_by_tag_name("a")
        if link_type == "Real Estate " or link_type == "Wanted " or link_type == "Offering ":
            for selected_elements in attribute_selected_elements :
                if selected_elements.get_attribute('data-event') == data_event and link_type == selected_elements.text.split('(')[0]:
                    link = selected_elements.get_attribute('href')
                    return link
            return ''
        elif link_type == "For Rent" or link_type == "Commercial & Other":
            for selected_elements in attribute_selected_elements :
                if selected_elements.find_elements_by_class_name("textContainer-4227985904") and selected_elements.find_elements_by_class_name("textContainer-4227985904")[0].find_element_by_tag_name('div').text == link_type:
                    link = selected_elements.get_attribute('href')
                    return link
            return ''

    # Getting Search Type Configuration And Clicking It
    # search_type = configuration.get("type").data
    logger.debug("Scraping Module : Searching for : " + str(search_type) + " Advertisements")

    if search_type == "Wanted" :
        search_type_link = extract_link("wantedSelection", "Wanted ")
    else : 
        search_type_link = extract_link("offeringSelection", "Offering ")
    
    if search_type_link != '' :
        browser.get(search_type_link)
    else :
        proceed_with_scraping = False
        logger.debug("Scraping Module : Stopping Scraping as no " + str(search_type) + " advertisements found")

    logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
    time.sleep(10)

    # Getting Real Estate Link And Clicking It
    logger.debug("Scraping Module : Fetching Real Estate Advertisements")
    real_estate_link = extract_link("ChangeCategory", "Real Estate ")
    if real_estate_link != '' :    
        browser.get(real_estate_link)
    else :
        proceed_with_scraping = False
        logger.debug("Scraping Module : Stopping Scraping as no Real Estate advertisements found")

    logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
    time.sleep(10)

    logger.debug("Scraping Module : Fetching Real Estate Advertisements For Rent")
    for_rent_link = extract_link("", "For Rent")
    if for_rent_link != '' :    
        browser.get(for_rent_link)
    else :
        proceed_with_scraping = False
        logger.debug("Scraping Module : Stopping Scraping as no Real Estate For Rent advertisements found")

    logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
    time.sleep(10)

    logger.debug("Scraping Module : Fetching Real Estate Advertisements For Commercial Spaces")
    commercial_space_link = extract_link("", "Commercial & Other")
    if commercial_space_link != '' :    
        browser.get(commercial_space_link)
    else :
        proceed_with_scraping = False
        logger.debug("Scraping Module : Stopping Scraping as no Real Estate For Rent - Commericial And Office Space advertisements found")

    logger.debug("Scraping Module : Waiting for Page to Load : Timeout 10 Seconds")
    time.sleep(10)

    """ Calculating Total No Of Pages To Be Parsed """

    if proceed_with_scraping :
        try :
            # Getting Selenium Element for Total No Of Results
            showing = browser.find_element_by_class_name("showing")
            showing_text = showing.text
            logger.debug("Scraping Module : Search Result For  : " + str(keyword.strip()) + " : is : " + str(showing_text))
            if showing_text != "No results" :
                total_advertisements = showing_text.split(' ')[5]
                total_advertisements = total_advertisements.replace(',','')
                logger.debug("Scraping Module : Total Advertisements Fetched : " + str(total_advertisements))
                current_advertisements = showing_text.split(' ')[3]
                logger.debug("Scraping Module : Current Advertisements Fetched : " + str(current_advertisements))
                total_pages = math.ceil(int(total_advertisements)/int(current_advertisements))
                logger.debug("Scraping Module : Total Pages To Be Parsed : " + str(total_pages))
            else :
                logger.debug("Scraping Module : No Appropriate Advertisements Found")
                logger.debug("Scraping Module : Moving On to Other Keyword If Any")
                total_pages = 0
        except Exception as e :
            logger.debug("Scraping Module : Exception in Fetching Total No Of Pages")
            print(e)
            logger.debug("Scraping Module : System Existing")
            total_pages = 0
            sys.exit()
        
        logger.debug("Scraping Module : Total Pages = " + str(total_pages))

        
        """ Fetching Advertisement Links """

        current_advertisment_links = []
        pages_traversed = 0

        # Getting Configured Date from the Configuration
        search_post_date = datetime.strptime(date_in_property, '%d/%m/%Y').date()
        logger.debug("Scraping Module : Configured Search Date is : " + str(search_post_date))

        if date_in_property == '01/01/1970' :
            logger.debug("Scraping Module : Calculating Previous 30 Days to Start Searching")
            today = date.today()
            search_post_date = today - timedelta(days=30)
            logger.debug("Scraping Module : Calculated Search Date is : " + str(search_post_date))

        # Looping Till All the Pages are Traversed
        while pages_traversed < total_pages :
            
            """ time.sleep(10) """
            
            # Getting Selenium Element for Advertisement
            advertisements = browser.find_elements_by_class_name("regular-ad")
            
            for ad in advertisements :
                wanted_ad = False
                ad_date = ad.find_element_by_class_name("date-posted").text
                if "ago" in ad_date :
                    wanted_ad = True
                elif "Yesterday" in ad_date :
                    today = date.today()
                    yesterday = today - timedelta(days=1)
                    if yesterday >= search_post_date :
                        wanted_ad = True
                else :
                    ad_posted_date = datetime.strptime(ad_date, '%d/%m/%Y').date()
                    if ad_posted_date >= search_post_date :
                        wanted_ad = True
                
                if wanted_ad :
                    advertisment_links.add(ad.find_element_by_tag_name("a").get_attribute('href'))
                    current_advertisment_links.append(ad.find_element_by_tag_name("a").get_attribute('href'))

            pages_traversed += 1
            logger.debug("Scraping Module : Pages Traversed So Far : " + str(pages_traversed))
            links_processed = len(current_advertisment_links)
            logger.debug("Scraping Module : Links Processed So Far : " + str(links_processed))
            next_page_url = ''

            if str(pages_traversed) != str(total_pages) and str(links_processed) == str(current_advertisements):
                pagination_element = browser.find_element_by_class_name("pagination")
            
                for link in pagination_element.find_elements_by_tag_name("a") :
                    if "Next" == link.get_attribute("title") :
                        next_page_url = link.get_attribute("href")
                        break
                browser.get(next_page_url)
            else :
                break

        logger.debug("Scraping Module : Total Links for : " + str(keyword) + " is : " + str(len(current_advertisment_links)))

        # Getting Search Box Selenium Element to Clear its Text before Inputting Next Text
        search_box = wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
        time.sleep(2)
        search_box.clear()
    else :
        browser.close()
        browser.quit()
    

logger.debug("Scraping Module : Starting Data Scraping")
extract = Extract()
logger.debug("Scraping Module : Final Processing For All Advertisements In Progress")
current_timestamp = extract.extract_data(browser, advertisment_links, finalTimestamp_in_property, HandleProperties(), logger, province_name, city_name)
updated_date = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")

location_dictionary = openFile("r", "")
province_dictionary = location_dictionary["province_dict"]
city_dictionary = location_dictionary["city_dict"]
province_name = province_dictionary.get(province_argument)
cities_json = city_dictionary.get(province_argument)
city_json = cities_json.get(city_argument)
city_name = city_json.get("name")

if type_argument == "w" :
    search_type = "Wanted"
    wanted_json = city_json.get("wanted")
    date_in_property = wanted_json["searchDate"]
    finalTimestamp_in_property = wanted_json.get("finalTimestamp")
elif type_argument == "o" :
    search_type = "Offering"
    offering_json = city_json.get("offering")
    date_in_property = offering_json["searchDate"]
    finalTimestamp_in_property = offering_json.get("finalTimestamp")

if type_argument == "w" :
    wanted_json["searchDate"] = str(updated_date)
    wanted_json["finalTimestamp"] = str(current_timestamp)
    city_json["wanted"] = wanted_json
elif type_argument == "o" :
    offering_json["searchDate"] = str(updated_date)
    offering_json["finalTimestamp"] = str(current_timestamp)
    city_json["offering"] = offering_json

cities_json[city_argument] = city_json
city_dictionary[province_argument] = cities_json
location_dictionary["province_dict"] = province_dictionary
location_dictionary["city_dict"] = city_dictionary

openFile("w", location_dictionary)
logger.debug("Scraping Module : Final Processing For All Advertisements Completed")
if proceed_with_scraping :
    browser.close()
    browser.quit()
