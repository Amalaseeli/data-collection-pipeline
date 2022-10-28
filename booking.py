from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def accept_cookies():
    driver=webdriver.Chrome()
    driver.get('https://www.booking.com/index.en-gb.html?label=gen173nr-1BCAEoggI46AdIM1gEaFCIAQGYAQm4ARfIAQzYAQHoAQGIAgGoAgO4AuLi8JoGwAIB0gIkNmU0ZThlYTMtOTUxZS00MWMyLWE2M2EtOGQyZDE2ODNjOGU22AIF4AIB&sid=cf65546d0da988fb447ff54e24cac061&keep_landing=1&sb_price_type=total&')
    driver.maximize_window()
    delay=10
    try:
        WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='onetrust-banner-sdk']")))
        print("Frame Ready!")
        driver.switch_to.frame('id="onetrust-banner-sdk"')
        accept_cookies_button=WebDriverWait(driver,delay).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='onetrust-accept-btn-handler']")))
        print("Accept Cookies Button Ready!")
        accept_cookies_button.click()# need to check................
        time.sleep(1)
    except TimeoutException:
        print("Loading took too much time!")

    return driver 

if __name__=='__main__':
    accept_cookies()