from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import unittest
import time
import datetime
import uuid
import json
import os

class Scrapper(unittest.TestCase):
    def __init__(self):
        self.driver=webdriver.Chrome()
        
    def _load_and_accept_cookies(self):
        driver=self.driver
        driver.maximize_window()
        driver.get('https://www.myprotein.com/')

        '''After signup it is popping up I am not robot window. So , As we know its change every time we just close the window.
        '''
        time.sleep(2)
        self.driver.find_element(By.ID, 'email').send_keys("am2027@gmail.com")
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
        

    def _scroll_down_website_page(self):
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
    
    def _search_product(self):
        driver=self.driver
        element=driver.find_element(By.NAME, 'search')
        element.click()
        time.sleep(1)
        element.send_keys('Protein Bars')
        element.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source)
        time.sleep(2)
       
    def _create_list_of_website_links(self)->list:
        '''Returns a list with all the links in the current page
            Returns
            -------
            link_list: list
        A list with all the links in the page'''
        
        web_element_list=self.driver.find_elements(By.XPATH, '//div[@class="athenaProductBlock_imageContainer"]/a')

        #container=WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="athenaProductBlock_imageContainer"]/a')))
        item_list=[]
        for element in web_element_list:
            item_link=element.get_attribute('href')
            item_list.append(item_link)
            
        print(len(set(item_list)))  
        return item_list

    def _retrieve_data(self,product_link):
        '''Return product properties'''
        driver=self.driver
        driver.maximize_window()
        driver.get(product_link)
        start_time=time.time()

        id=str(uuid.uuid4())
        Timestamp=datetime.datetime.fromtimestamp(start_time).strftime('%Y_%b_%d_%H_%M_%S_%f_%p')
        img_list=[] 
        fp=datetime.datetime.fromtimestamp(start_time).strftime('%d%m%Y_%f')
        img_li=driver.find_elements(By.CLASS_NAME, "athenaProductImageCarousel_thumbnail")
        for img in img_li:
            img_list.append(img.get_attribute('src'))
            self._download_img(product_link,fp)
            
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
            id,img_list,product_name,price,flavour,Timestamp=self._retrieve_data(link)
            data_dict={'id':'','item':{},'Timestamp':''}
            
            data_dict['id']=id
            data_dict['item']['img_list']=img_list
            data_dict['item']['product_name']=product_name
            data_dict['item']['price']=price
            data_dict['item']['flavour']=flavour
            data_dict['Timestamp']=Timestamp
            print(data_dict)
            filename=data_dict['id']
            self._create_folder_json(filename)
            self._write_json(data_dict,filename)
            return data_dict

    def _create_folder_json(self,filename):
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
        if not os.path.exists(f'raw_data/{filename}'):
            os.makedirs(f'raw_data/{filename}')

    def _create_folder_images(self):
        if not os.path.exists('images'):
            os.makedirs('images')
    
    def _write_json(self,data,filename):
        with open(f'raw_data/{filename}/data.json', 'w') as file:
            json.dump(data, file, indent = 4)

    def _get_25_item_properties(self):
        link_list=[]
        item_properties=[]
        self._search_product()
        while True:
            link_list.extend(self._create_list_of_website_links())
            for i in range(25):
                item_link=link_list[i]
                item_properties.append(self.update_data_dict(item_link))
            self.driver.get('https://www.myprotein.com/nutrition/healthy-food-drinks/protein-bars.list?search=protein+bar')
            self.click_next_buton()
            return item_properties

    def _click_next_buton(self):
        next_button=self.driver.find_element(By.XPATH, '//ul[@class="responsivePageSelectors"]')
        next=next_button.find_element(By.XPATH, './/button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]')
        click_next_button=next.find_element(By.XPATH, "./*[name()='svg']")
        ActionChains(self.driver).move_to_element(click_next_button).click().perform()
        time.sleep(5)
        
    def _download_img(self,link,filepath):
        self._create_folder_images()
        img_data = requests.get(link).content
        with open(f'images/{filepath}.jpg', 'wb') as handler:
            handler.write(img_data)
  
    def quit(self):
        self.driver.quit()

if __name__=="__main__":
    webpage=Scrapper()
    webpage._load_and_accept_cookies()
    webpage._get_25_item_properties()
    
    webpage.quit()


   