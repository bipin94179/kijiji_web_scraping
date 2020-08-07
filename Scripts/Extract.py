import time
from datetime import datetime
import csv
import re
import pathlib
import os

class Extract :

    def extract_data(self, browser, advertisment_links, finalTimestamp, fetchProperties, logger, province_name, city_name) :

        current_timestamp = 0

        if finalTimestamp != "0" :
            final_timestamp = datetime.strptime(finalTimestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

        row=[]

        project_directory_path = pathlib.Path().absolute()
        data_directory_path = str(project_directory_path) + "/Data/"
        city_name_split_list = city_name.split(' ')
        final_city_name = ''
        for name in city_name_split_list :
            if name != "/" :
                if final_city_name != '' :
                    final_city_name = final_city_name + "-"
                final_city_name = final_city_name + name.strip()
        fileName = datetime.now().strftime(str(data_directory_path) + "Data_" + province_name + "_" + final_city_name + "_" + '_%d_%m_%Y_%H_%M_%S' + '.csv')
        
        with open(fileName, 'w+', newline='') as csvfile:
            output_csv = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')

            row.append("Unique Id")
            row.append("Time Posted")
            row.append("Page Link")
            row.append("Title")
            row.append("Description")
            row.append("Address")
            row.append("City")
            row.append("Postal Code")
            row.append("Phone No")
            row.append("Email")

            output_csv.writerow(row)
            row.clear()
            count = 0

            for link in advertisment_links:
                to_be_added = False
                browser.get(link)
                time.sleep(2)

                date_element = browser.find_element_by_class_name("datePosted-383942873")
                date_span_element = date_element.find_element_by_tag_name("time")
                timestamp = date_span_element.get_attribute("datetime")
                formatted_timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

                if current_timestamp == 0 :
                        current_timestamp = timestamp

                if finalTimestamp == "0" :
                    to_be_added = True
                elif finalTimestamp != "0" :
                    if formatted_timestamp > final_timestamp :
                        to_be_added = True
                
                if to_be_added :
                    
                    page_link = link
                    title = browser.find_element_by_class_name("title-2323565163").text
                    description = browser.find_element_by_class_name("descriptionContainer-3544745383").find_element_by_tag_name("div").text
                    address = browser.find_element_by_class_name("locationContainer-2867112055").find_element_by_class_name("address-3617944557").text

                    postal_code_pattern = re.search("[A-Za-z][0-9][A-Za-z](\s){0,1}[0-9][A-Za-z][0-9]", address)
                    if postal_code_pattern != None :
                        codes = postal_code_pattern.group()
                    else :
                        codes = ''

                    city = ((address.upper().replace(codes.upper(), '').replace('CANADA', '')).replace(",", '')).strip()

                    email_pattern = re.compile('\w+@\w+\.[a-z]{3}')
                    emails = email_pattern.findall(description)
                    mails = ''
                    if len(emails) > 0 :
                        for email in emails :
                            mails += email
                            mails += "\n"

                    phone_number_pattern = re.compile('[0-9]{3}?[-\s]?[0-9]{3}[-\s]?[0-9]{4}')
                    phone_numbers = phone_number_pattern.findall(description)
                    numbers = ''
                    if len(phone_numbers) > 0 :
                        for phone_number in phone_numbers :
                            numbers += phone_number
                            numbers += "\n"

                    link_attributes = page_link.split('/')

                    row.append(link_attributes[len(link_attributes)-1])
                    row.append(formatted_timestamp)
                    row.append(page_link)
                    row.append(title)
                    row.append(description)
                    row.append(address)
                    row.append(city)
                    row.append(codes)
                    row.append(numbers)
                    row.append(mails)

                    output_csv.writerow(row)
                    row.clear()
                    count += 1
                    if count == 10 :
                        count = 0
                        logger.debug("Extract Module : Process Still Running.....")

        return current_timestamp
        
        
