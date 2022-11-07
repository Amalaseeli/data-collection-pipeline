from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest
import time

class Scrapper(unittest.TestCase):
    def __init__(self):
        self.driver=webdriver.Chrome()
        
    def load_and_accept_cookies(self):
        driver=self.driver
        driver.maximize_window()
        driver.get('https://www.myprotein.com/')

        '''After signup it is popping up I am not robot window. So , As we know its change every time we just close the window.
        for signup the following code will works
        ...............
         # self.driver.find_element(By.ID, 'email').send_keys("amalremi07@gmail.com")
        # self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_newsletterForm_submit"]').click()
        '''
        
        self.driver.find_element(By.ID, 'email').send_keys("amalremi07@gmail.com")
        self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_newsletterForm_submit"]').click()
        time.sleep(5)
        self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_close_button"]').click()
        # self.driver.find_element(by=By.XPATH, value='//*[@class="recaptcha-checkbox-border"]/div[4]').click()
        
        #Clcik accept cookies
        
        try:
            accept_cookies_button=self.driver.find_element(by=By.XPATH, value='//button[@class="cookie_modal_button"]')
            accept_cookies_button.click()
        except AttributeError:
            accept_cookies_button=self.driver.find_element(by=By.XPATH, value='//button[@class="cookie_modal_button"]')
            accept_cookies_button.click()
        
        time.sleep(2)
        self.scroll_down_website_page()
        time.sleep(2)

    def scroll_down_website_page(self):
        SCROLL_PAUSE_TIME = 2.5
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
             # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
               # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def search_product(self):
        driver=self.driver
        element=driver.find_element(By.NAME, 'search')
        element.click()
        time.sleep(1)
        element.send_keys('Protein Bars')
        element.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source)
    
    def get_links(self):
        self.search_product()
        container=self.driver.find_elements(By.XPATH, '//a[@class="athenaProductBlock_linkImage"]')
        item_list=[]
        #print(container)
        for link in container:
            item_link=link.get_attribute('href')
            item_list.append(item_link)
        # print(set(item_list))
        # print(len(set(item_list)))  
        return item_list 

    def retrive_data(self):
        link1=self.get_links()[0] 
        driver=self.driver
        driver.maximize_window()
        driver.get(link1) 
        img=driver.find_element(By.CLASS_NAME, "athenaProductImageCarousel_image").get_attribute('src')
        product_name=driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div[2]/div/div[1]/div[2]/div/h1').text
        #flavour=driver.find_element(By.XPATH, '//*[@id="athena-product-variation-dropdown-5"]')
        select_item=Select(driver.find_elements(By.XPATH, '//*[@id="athena-product-variation-dropdown-5"]'))
        # all_options= [o.get_attribute('value') for o in select_item]
        # for x in all_options:
        #     select_item.select_by_value(x)
            
        all_options=select_item.find_element(By.TAG_NAME, 'option')
        for option in all_options:
            print(option.get_attribute('value'))
        
        time.sleep(3)

        print(img)
        print(product_name)

    def quit(self):
        self.driver.quit()

if __name__=="__main__":
    webpage=Scrapper()
    webpage.load_and_accept_cookies()
    webpage.retrive_data()
    webpage.quit()