import logging
from datetime import datetime
from datetime import date
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from FetchProperties import FetchProperties
from Extract import Extract
import math
from selenium.webdriver.chrome.options import Options  

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
# chrome_options = Options()  
# chrome_options.add_argument("--headless")
# browser = webdriver.Chrome(options=chrome_options)
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.get(url)
browser.maximize_window()

""" Updating Location """

time.sleep(10)

province = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, configuration.get("province").data)))
province.click()

print("Province is : ", configuration.get("province").data)

area = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, configuration.get("area").data)))
area.click()

print("Area is : ", configuration.get("area").data)

location_update = wait.until(EC.element_to_be_clickable((By.ID, 'LocUpdate')))
location_update.click()

""" Searching Keywords """

time.sleep(10)

keywords = (configuration.get("keyword").data).split('||')
advertisment_links = []

print("Keywords", keywords)

for keyword in keywords :

    print("Searching for : ", keyword)

    search_box = wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
    search_box.send_keys(keyword)

    search_button = wait.until(EC.element_to_be_clickable((By.NAME, 'SearchSubmit')))
    search_button.click()

    time.sleep(10)

    """ Get Wanted Advertisements """

    wanted_link = ''
    real_estate_link = ''
    for_rent_link = ''
    office_link = ''

    def extract_link (data_event, link_type) :
        attribute_selected_elements = browser.find_elements_by_tag_name("a")
        for selected_elements in attribute_selected_elements :
            if selected_elements.get_attribute('data-event') == data_event and link_type == selected_elements.text.split('(')[0]:
                link = selected_elements.get_attribute('href')
                print(link)
                return link
        return ''

    real_estate_link = extract_link("ChangeCategory", "Real Estate ")
    if real_estate_link != '' :    
        browser.get(real_estate_link)

    time.sleep(10)
    for_rent_link = extract_link("ChangeCategory", "For Rent ")
    if for_rent_link != '' :    
        browser.get(for_rent_link)

    time.sleep(10)
    office_link = extract_link("ChangeCategory", "Commercial & Office Space for Rent ")
    if office_link != '' :    
        browser.get(office_link)

    time.sleep(10)
    wanted_link = extract_link("wantedSelection", "Wanted ")
    if wanted_link != '' :
        browser.get(wanted_link)



    """ Fetching Total No Of Pages """

    try :
        showing = browser.find_element_by_class_name("showing")
        showing_text = showing.text
        if showing_text != "No results" :
            total_advertisements = showing_text.split(' ')[5]
            current_advertisements = showing_text.split(' ')[3]
            total_pages = math.ceil(int(total_advertisements)/int(current_advertisements))
            print("Total Pages = " + str(total_pages))
        else :
            total_pages = 0
    except :
        total_pages = 0

    
    """ Fetching Advertisement Links """

    current_advertisment_links = []
    pages_traversed = 0
    date_in_property = configuration.get("searchDate").data
    search_post_date = datetime.strptime(date_in_property, '%d/%m/%Y').date()
    if date_in_property == '01/01/1970' :
        today = date.today()
        search_post_date = today - timedelta(days=30)

    while pages_traversed < total_pages :
        
        time.sleep(10)
        
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
                advertisment_links.append(ad.find_element_by_tag_name("a").get_attribute('href'))
                current_advertisment_links.append(ad.find_element_by_tag_name("a").get_attribute('href'))

        pages_traversed += 1
        links_processed = len(current_advertisment_links)
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

    print("Total Links for : ", keyword, " is : ", len(current_advertisment_links))
    search_box = wait.until(EC.element_to_be_clickable((By.ID, 'SearchKeyword')))
    time.sleep(2)
    search_box.clear()
    

print("Starting Data Scraping")
extract = Extract()
extract.extract_data(browser, advertisment_links, configuration.get("finalTimestamp").data, fetchProperties)

updated_date = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
fetchProperties.write_properties('searchDate', updated_date)

