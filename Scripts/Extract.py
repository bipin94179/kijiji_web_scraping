import time
from datetime import datetime

class Extract :

    def extract_data(self, browser, advertisment_links, finalTimestamp) :

        title = []
        description = []
        phone_no = []
        email = []
        city = []
        postal_code = []
        page_link = []
        current_timestamp = 0

        if finalTimestamp != "0" :
            final_timestamp = datetime.strptime(finalTimestamp, '%b %d, %Y %I:%M %p') 
            print(final_timestamp)

        for link in advertisment_links:
            browser.get(link)
            time.sleep(10)

            timestamp = browser.find_element_by_class_name("datePosted-383942873").find_element_by_tag_name("span").get_attribute("title")
            print(timestamp)
            formatted_timestamp = datetime.strptime(timestamp, '%b %d, %Y %I:%M %p')
            print(formatted_timestamp)
            if finalTimestamp == "0" and current_timestamp == 0:
                current_timestamp = timestamp
                print(current_timestamp)
            elif finalTimestamp != "0" :
                if formatted_timestamp > final_timestamp :
                    title.append(browser.find_element_by_class_name("title-2323565163").text)
                    print(browser.find_element_by_class_name("title-2323565163").text)
        pass