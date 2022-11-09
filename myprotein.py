from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest
import time
import datetime
import uuid


class Scrapper(unittest.TestCase):
    def __init__(self):
        self.driver=webdriver.Chrome()
        
        
    def load_and_accept_cookies(self):
        driver=self.driver
        driver.maximize_window()
        driver.get('https://www.myprotein.com/')

        '''After signup it is popping up I am not robot window. So , As we know its change every time we just close the window.
        '''
        time.sleep(2)
        self.driver.find_element(By.ID, 'email').send_keys("amalremi07@gmail.com")
        self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_newsletterForm_submit"]').click()
        time.sleep(5)
        self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_close_button"]').click()
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
        time.sleep(2)
        self.driver.execute_script("window.scrollTo(0, 2000);")
        #self.filter_data()

    def get_links(self)->list:
        '''Returns a list with all the links in the current page
            Returns
            -------
            link_list: list
        A list with all the links in the page'''
        self.search_product()
        container=self.driver.find_elements(By.XPATH, '//div[@class="athenaProductBlock_imageContainer"]/a')
        
        item_list=[]
        for link in container:
            item_link=link.get_attribute('href')
            item_list.append(item_link)
        # print(set(item_list))
        # print(len(set(item_list)))  
        return item_list 

    def filter_data(self):
        #click vanila flavour and Gluten free
        self.driver.find_element(By.XPATH, '//*[@id="home"]/div[5]/div[1]/aside/div/div/div[2]/div[2]/div[3]/div[2]/fieldset/label[39]/input').click
        self.driver.execute_script("window.scrollTo(0, 1200);")
        self.driver.find_element(By.XPATH,'//*[@id="home"]/div[5]/div[1]/aside/div/div/div[2]/div/div[4]/div[2]/fieldset/label[1]/input').click

    def retrive_data(self,product_link):
        '''Return product properties'''
        driver=self.driver
        driver.maximize_window()
        driver.get(product_link)
        start_time=time.time()

        id=str(uuid.uuid4())
        print(id)
        Timestamp=datetime.datetime.fromtimestamp(start_time).strftime('%Y_%b_%d_%H_%M_%S_%f_%p')
        print(Timestamp)
        img_list=[] 
        img_li=driver.find_elements(By.CLASS_NAME, "athenaProductImageCarousel_thumbnail")
        for img in img_li:
             img_list.append(img.get_attribute('src'))

        product_name=driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div[2]/div/div[1]/div[2]/div/h1').text
        price=driver.find_element(By.XPATH,'//p[@class="productPrice_price  "]').text
        select_item=Select(driver.find_element(By.XPATH, '//*[@id="athena-product-variation-dropdown-5"]'))
        all_options=select_item.options
        flavour=[]
        for option in all_options:
            flavour.append(option.text)
        
        
        
        time.sleep(3)
        return id,img_list,product_name,price,flavour,Timestamp

    def update_data_dict(self,link):
            id,img_list,product_name,price,flavour,Timestamp=self.retrive_data(link)
            data_dict={}
            data_dict['id']=id
            data_dict['img_list']=img_list
            data_dict['product_name']=product_name
            data_dict['price']=price
            data_dict['flavour']=flavour
            data_dict['Timestamp']=Timestamp
            print(data_dict)
            return data_dict

    def get_4_item_properties(self):
        link_list=[]
        item_properties=[]
        link_list.extend(self.get_links())
        for i in range(4):
            item_link=link_list[i]
            item_properties.append(self.update_data_dict(item_link))
        print(item_properties)

    def click_next_page(self):
        Page_list=self.driver.find_elements(By.CLASS_NAME, '//*[@id="mainContent"]/div[4]/nav/ul')
        list=Page_list[0].find_elements('li')
        for li in list:
            link=li.__getattribute__('src')
            print(link)


    def quit(self):
        self.driver.quit()

if __name__=="__main__":
    webpage=Scrapper()
    webpage.load_and_accept_cookies()
    webpage.get_4_item_properties()
    webpage.quit()


   