import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import env


class SignupTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def test_signup(self):
        self.driver.get(f"{env.host}/login")
        self.assertIn("Index Insurance", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT,'Create Account')
        elem.click()
        self.assertIn("address", self.driver.page_source)
        self.assertIn("phrase", self.driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
