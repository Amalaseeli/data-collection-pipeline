
from re import L
from tkinter import Frame
from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
''' 
If couldn't move to specific path....
you can still use
...............

from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install()) 
'''

driver.get('https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&view_type=list')
time.sleep(2)
# self.driver = webdriver.Chrome(ChromeDriverManager().install())
# my_path=driver.find_element(by=By.XPATH, value='//div[@id="css-uti5dl elit0xq13"]')

# new_path = my_path.find_element(by=By.XPATH, value='./div')

assert "New Homes for Sale in London - Zoopla" in driver.title

def accept_cookies():
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
    time.sleep(2)
    return driver

def get_links()->list:
    '''Returns a list with all the links in the current page
        Returns
        -------
        link_list: list
    A list with all the links in the page'''

    container=driver.find_element(By.XPATH, "//div[@class='css-1kk52wv etglsof6']")
    prop_list=container.find_elements(By.XPATH, ".//div[contains(@id, 'listing_627')]")
    link_list=[]
    for house_property in prop_list:
        a_tag=house_property.find_element(By.TAG_NAME, 'a')
        link=a_tag.get_attribute('href')
        link_list.append(link)
        # print(f'There are {len(link_list)} properties in this page')
        # print(link_list)
    return link_list
# print(link)
# driver.get(link)

def get_properties(link):
    dict_properties={'price':[],'Address':[],'bedrooms':[]}
    for link in big_list:
        driver.get(link)
        price=driver.find_element(By.XPATH, "//p[@data-testid='price']").text
        dict_properties['price'].append(price)
        address=driver.find_element(By.XPATH, '//address[@data-testid="address-label"]').text
        dict_properties['Address'].append(address)
        bedrooms=driver.find_element(By.XPATH, '//div[@class="c-PJLV c-PJLV-kQvhQW-centered-true c-PJLV-iPJLV-css"]').text
        dict_properties['Bedrooms'].append(bedrooms)
    return dict_properties

big_list=[]   
def get_five_page_of_details(page_link):
    
    for i in range(5):
        big_list.extend(get_links())
        link=page_link[i]
        get_properties(link)
        # button=driver.find_element(By.XPATH, '//li[@class="css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]//a')
        # button.click()
# house_property=driver.find_element(by=By.XPATH, value='//*[@class_name="c-jiEdYR"')
if __name__=="__main__":
    

    # house_property=driver.find_element(By.XPATH, "//div[@id='listing_62736450']")
    
    
    driver=accept_cookies()
    get_links()



    
    
    # container=driver.find_element(By.XPATH, "//div[@class='css-1kk52wv etglsof6']")
    # listings=container.find_elements(By.XPATH, ".//div[contains(@id, 'listing_627')]")
    # for list in listings:
    #     a_tag=list.find_elment(by=By.TAG_NAME,value="a")
    #     link=a_tag.get_attribute('href')
    #     print(link)
    # a_tag_container.find_element(by=By.TAG_NAME, value="a" )
    # 
    # print(link)
    #print(listings)
    driver.quit()