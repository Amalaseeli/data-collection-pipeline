
from re import L
from tkinter import Frame
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time

''' 
If couldn't move to specific path....
you can still use
...............

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install()) 
'''


class scrapper:

    def accept_cookies(self)-> webdriver.Chrome:
        driver = webdriver.Chrome()
        driver.get('https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&view_type=list')
        time.sleep(2)
        # assert "New Homes for Sale in London - Zoopla" in driver.title
        try:
            driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()
            driver.switch_to.default_content()

        except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame

            accept_cookies_button = driver.find_element(by=By.XPATH, value='//*[@id="save"]')
            accept_cookies_button.click()
            driver.switch_to.default_content()

        except:
            pass
        
        return driver
        
    def get_links(self,driver: webdriver.Chrome)->list:
        '''Returns a list with all the links in the current page
            Returns
            -------
            link_list: list
        A list with all the links in the page'''

        container=driver.find_element(By.XPATH, "//div[@data-testid='regular-listings']")
        prop_list=container.find_elements(By.XPATH, ".//div[contains(@id, 'listing_627')]")
        # print(prop_list)
        link_list=[]
        for house_property in prop_list:
            a_tag=house_property.find_element(By.TAG_NAME, 'a')
            link=a_tag.get_attribute('href')
            link_list.append(link)
            # print(f'There are {len(link_list)} properties in this page')
            # print(link_list)
        return link_list


    def get_properties(self,link):
        dict_properties={}
        
        driver.get(link)
        price=driver.find_element(By.XPATH, "//p[@data-testid='price']").text
        dict_properties['price']=price
        address=driver.find_element(By.XPATH, '//address[@data-testid="address-label"]').text
        dict_properties['Address']=address
        # bedrooms=driver.find_element(By.XPATH, '//span[@class="c-PJLV"]').text
        # dict_properties['Bedrooms']=bedrooms
        return dict_properties 




        # button=driver.find_element(By.XPATH, '//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]//a')
        # button.click()
# house_property=driver.find_element(by=By.XPATH, value='//*[@class_name="c-jiEdYR"')
if __name__=="__main__":
    pro=scrapper()
    driver=pro.accept_cookies()
    big_list=[]   
    big_list.extend(pro.get_links(driver))
    property_list=[]
    for i in range(3):
        p_link=big_list[i]
        property=pro.get_properties(p_link)
        property_list.append(property)
    # print(page_link_list)
    print(property_list)
    driver.quit()



    
    

   