class Extract :

    def getDetails(self, title, description, phone_no, email, city, postal_code, page_link, browser) :
        
        print(browser.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div/div[5]/div[2]/div[4]/div[1]/div/h3").text)
        
        print(browser.find_element_by_xpath("/html/body/div[3]/div[3]/div/div/div/div[5]/div[2]/div[4]/div[1]/div/div").text)
        pass