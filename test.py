import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class AmazonSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_search_in_Amazon_Com(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("https://www.amazon.com/")
        time.sleep(2)
        self.page_title=driver.title
        print(self.page_title)
        self.assertIn("Amazon", driver.title)
        self.scroll_website()    
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")#Scroll down the page
        time.sleep(1)
        elem = driver.find_element(By.XPATH, "//*[@id='twotabsearchtextbox']")
        elem.click()
        time.sleep(1)
        elem.send_keys("computer")
        elem.send_keys(Keys.RETURN)
        self.assertNotIn("No results found.", driver.page_source) 


    #If you want to scroll to a page with infinite loading, like social network ones, facebook etc.
    def scroll_website(self):
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

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()



