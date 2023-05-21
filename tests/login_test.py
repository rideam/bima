import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import env


class LoginTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def test_login(self):
        # driver = self.driver
        self.driver.get(f"{env.host}/login")
        self.assertIn("Index Insurance", self.driver.title)
        elem = self.driver.find_element(By.NAME, "passphrase")
        elem.send_keys(env.account_two_memonic)
        elem.send_keys(Keys.RETURN)
        self.assertIn("Account Details", self.driver.page_source)
        self.assertIn(env.account_two_address, self.driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
