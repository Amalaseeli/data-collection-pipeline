from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome()
driver.get('https://www.amazon.com/')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

search_bar=driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
search_bar.click()
driver.close()
# driver.quit()
# class scrapper:
#     def __init__(self) -> None:
#         self.driver=webdriver.Chrome()

#     def get_data(self):
#         driver=self.driver
#         driver.get('https://www.amazon.com/')
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     def quit(self):
#         self.driver.quit()

# if __name__=='__main__':
#     pass
