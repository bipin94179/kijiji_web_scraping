import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select


class Extract:
    url = "https://www.kijiji.ca/v-room-rental-roommate/cowichan-valley-duncan/want-to-rent/1509072438"

    def extract_data(self):

        url = "https://www.kijiji.ca/v-room-rental-roommate/cowichan-valley-duncan/want-to-rent/1509072438"

        title = []
        description = []
        phone_no = []
        email = []
        city = []
        postal_code = []
        page_link = []
        current_timestamp = 0

        browser = webdriver.Chrome()
        wait = WebDriverWait(browser, 10)
        browser.get(url)
        browser.maximize_window()

        time.sleep(10)

        timestamp = browser.find_element_by_class_name(
            "datePosted-383942873").find_element_by_tag_name("span").get_attribute("title")


extract = Extract()
extract.extract_data()
