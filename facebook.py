'''Working with accept_cookies and login form'''



from tkinter import E
from selenium import webdriver
from selenium.webdriver.common.by import By

driver=webdriver.Chrome()
driver.get("https://www.facebook.com/")
driver.maximize_window()
print(driver.current_url)
def accept_cookies():
    try:
        accept_cookies_button=driver.find_element(by=By.XPATH, value="//button[@data-testid='cookie-policy-manage-dialog-accept-button']")
        accept_cookies_button.click()
        
    except AttributeError:
       
        accept_cookies_button=driver.find_element(by=By.XPATH, value='//button[@data-testid="cookie-policy-manage-dialog-accept-button"]')
        accept_cookies_button.click()
        
    except:
            pass
        
    return driver


def navigate_form():
    driver.find_element(By.ID, 'email').send_keys("amalremi07@gmail.com")
    driver.find_element(By.ID,'pass').send_keys("Amalre!")
    driver.find_element(By.NAME,'login').click()
    

if __name__=='__main__':
    accept_cookies()
    navigate_form()