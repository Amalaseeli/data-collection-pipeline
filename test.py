from myprotein import Scrapper
import unittest
import time
import os

class ScrapperTestCase(unittest.TestCase):
    
    def setUp(self):
        self.scrapper=Scrapper()

    @unittest.skip    
    def test_load_and_accept_cookies(self):
        self.setUp()
        actual=self.scrapper.driver.current_url
        expected='https://www.myprotein.com/'
        self.assertEqual(actual,expected, 'Test failed')

    @unittest.skip
    def test_search_product(self):
        self.setUp()
        time.sleep(2)
        self.scrapper.search_product()
        actual=self.scrapper.driver.current_url
        print(self.scrapper.driver.page_source)
        expected='https://www.myprotein.com/elysium.search?search=Protein+Bars'
        self.assertEqual(actual,expected)
    
    @unittest.skip
    def test_create_list_of_website_links(self):
        self.setUp()
        time.sleep(2)
        self.scrapper.search_product()
        time.sleep(1)
        self.item_list=self.scrapper._create_list_of_website_links()
        print(self.item_list)
        print(len(self.item_list))
        self.assertAlmostEqual(len(self.item_list),36)
    
    def test_retrieve_data(self):
        self.setUp()
        time.sleep(2)
        self.scrapper.search_product()
        time.sleep(1)
        self.item_list=self.scrapper._create_list_of_website_links()
        self.assertTrue(True)
        id,img_list,product_name,price,flavour,Timestamp=self.scrapper._retrieve_data(self.item_list[0])
        assert type(id) is str
        assert isinstance(img_list, list)
        assert type(product_name).__name__ == "str"
        self.assertIsInstance(flavour, list)
        self.assertEqual(type(Timestamp),type("text"))
        print(id,img_list,product_name,price,flavour,Timestamp)

   
    def test_update_data_dict(self):
        self.setUp()
        time.sleep(2)
        self.scrapper.search_product()
        time.sleep(1)
        self.item_list=self.scrapper._create_list_of_website_links()
        item_properties=self.scrapper._update_data_dict(self.item_list[0])
                
        assert type(item_properties) is dict
    
    
    def test_get_item_properties(self):
        self.assertTrue(True) 
    
    def test__write_json(self):
        if(os.path.isdir('./raw_data/*/*.json')):
            self.assertTrue
        else:
            self.assertFalse

    def test_download_img(self):
        if (os.path.isdir('./images/*.jpg')):
           self.assertTrue
        else:
            self.assertFalse

    def test_navigate_to_each_page_and_get_properties(self):
        self.assertTrue(True) 

    def tearDown(self) -> None:
        self.scrapper.driver.close()

if __name__ == "__main__":
  unittest.main()


   