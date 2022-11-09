from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import unittest
import time

class Scrapper(unittest.TestCase):
    def __init__(self):
        self.driver=webdriver.Chrome()
        self.data_dict={"img":[],'product_name':'','price':'','flavour':[]  }
        
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

    def filter_data():
        pass
    
    def retrive_data(self,link):
        driver=self.driver
        driver.maximize_window()
        driver.get(link)
        img_list=[] 
        # img_container=driver.find_element(By.CLASS_NAME, 'athenaProductImageCarousel_listItem')
        # img_li=img_container.find_element(By.CLASS_NAME, "athenaProductImageCarousel_image").get_attribute('src')
        # for img in img_li:
        #     img_list.append(img)
        
        img=driver.find_element(By.CLASS_NAME, "athenaProductImageCarousel_image").get_attribute('src')
        
        product_name=driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div[2]/div/div[1]/div[2]/div/h1').text
        #dict_properties['product_name']=product_name
        price=driver.find_element(By.XPATH,'//p[@class="productPrice_price  "]').text
        #dict_properties['price']=price
        select_item=Select(driver.find_element(By.XPATH, '//*[@id="athena-product-variation-dropdown-5"]'))
        all_options=select_item.options
        flavour=[]
        for option in all_options:
            flavour.append(option.text)
        #dict_properties['flavour']=flavour
        time.sleep(3)
        # print(img)
        # print(product_name)
        # print(flavour)
        return img,product_name,price,flavour

    def update_data_dict(self,link):
            img_list,product_name,price,flavour=self.retrive_data(link)
            self.data_dict['img_list']=img_list
            self.data_dict['product_name']=product_name
            self.data_dict['price']=price
            self.data_dict['flavour']=flavour
            return self.data_dict
    
    def quit(self):
        self.driver.quit()

if __name__=="__main__":
    webpage=Scrapper()
    webpage.load_and_accept_cookies()
    link_list=[]
    item_properties=[]
    link_list.extend(webpage.get_links())
    for i in range(4):
        item_link=link_list[i]
        item_properties.append(webpage.update_data_dict(item_link))
    print(item_properties)

    webpage.quit()


    #get_36_links
    #return img,price,flavour
    #dictonary prop