from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Scrapper:
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
        time.sleep(2)
        try:
            accept_cookies_button=self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_close_button"]')
            accept_cookies_button.click()
        except AttributeError:
            accept_cookies_button=self.driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_close_button"]')
            accept_cookies_button.click()
        #Clcik accept cookies
        time.sleep(2)
        self.driver.find_element(by=By.XPATH, value='//button[@class="cookie_modal_button"]').click()
        time.sleep(2)
        self.scroll_down()
        time.sleep(2)

    def scroll_down(self):
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

    def quit(self):
        self.driver.quit()

if __name__=="__main__":
    webpage=Scrapper()
    webpage.load_and_accept_cookies()
    webpage.quit()