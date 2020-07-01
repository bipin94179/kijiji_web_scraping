import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
import re
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)


class Extract:
    url = "https://www.kijiji.ca/v-room-rental-roommate/cowichan-valley-duncan/want-to-rent/1509072438"

    def extract_data(self):

        url = "https://www.kijiji.ca/v-room-rental-roommate/cowichan-valley-duncan/want-to-rent/1509072438"

        # title = []
        # description = []
        # phone_no = []
        # email = []
        # city = []
        # postal_code = []
        # page_link = []

        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 10)
        browser.get(url)
        browser.maximize_window()

        time.sleep(10)

        timestamp = browser.find_element_by_class_name(
            "datePosted-383942873").find_element_by_tag_name("time").get_attribute("datetime")

        title = browser.find_element_by_class_name(
            "itemTitleWrapper-4111598823").find_element_by_class_name("title-2323565163").text

        raw_description = browser.find_element_by_class_name(
            "descriptionContainer-3544745383").find_element_by_tag_name("p").text

        city_postalcode = browser.find_element_by_class_name("itemMeta-4167503528").find_element_by_class_name(
            "locationContainer-2867112055").find_element_by_class_name("address-3617944557").text

        current_timestamp = datetime.now()

        # method to be implemented to extract city and postal code
        city, postal_code = self.extract_city_postcode(city_postalcode)

        page_link = url

        arr = []
        arr.extend([timestamp, title, city, postal_code,
                    current_timestamp, page_link])

        print(arr)

    def extract_city_postcode(self, input_text):
        input_text_upper = input_text.upper()
        print(input_text_upper)
        postal_code_match = re.search(
            "[A-Z][0-9][A-Z](\s){0,1}[0-9][A-Z][0-9]", input_text_upper)
        postal_code = postal_code_match.group()
        print('postal code', postal_code, sep=" ~ ")

        input_text_upper_1 = input_text_upper.replace(postal_code, '')
        city = ((input_text_upper_1.replace(
            'CANADA', '')).replace(",", '')).strip()

        print(city)
        return city, postal_code

    def extract_phone_email(self, raw_description):
        pass


extract = Extract()
extract.extract_data()
