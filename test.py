from selenium import webdriver
from myprotein import Scrapper
import unittest
import time
from selenium.webdriver.support.ui import WebDriverWait
# from unittest.mock import patch

class ScrapperTestCase(unittest.TestCase):
    
    def setUp(self):
        self.scrapper=Scrapper()
        
    def test_load_and_accept_cookies(self):
        self.scrapper.load_and_accept_cookies()
        actual=self.scrapper.driver.current_url
        expected='https://www.myprotein.com/'
        self.assertEqual(actual,expected, 'Test failed')

    def test_search_product(self):
        self.scrapper.load_and_accept_cookies()
        time.sleep(2)
        self.scrapper.search_product()
        actual=self.scrapper.driver.current_url
        expected='https://www.myprotein.com/elysium.search?search=Protein+Bars'
        self.assertEqual(actual,expected)
    
    def test_create_list_of_website_links(self):
        self.scrapper.load_and_accept_cookies()
        time.sleep(2)
        self.scrapper.search_product()
        time.sleep(1)
        self.item_list=self.scrapper._create_list_of_website_links()
        print(self.item_list)
        print(len(self.item_list))
        self.assertAlmostEqual(len(self.item_list),36)

if __name__ == "__main__":
  unittest.main()


   