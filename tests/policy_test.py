import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import env


class PolicyListTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def test_policy_list(self):
        driver = self.driver
        driver.get(f"{env.host}/login")
        driver.implicitly_wait(0.5)
        self.assertIn("Index Insurance", driver.title)
        elem = driver.find_element(By.NAME, "passphrase")
        elem.send_keys(env.account_two_memonic)
        elem.send_keys(Keys.RETURN)
        join_policy = driver.find_element(By.ID, "joinpolicy")
        join_policy.click()
        driver.execute_script("return jQuery.active == 0")
        self.assertIn("Policies", driver.page_source)
        self.assertIn("Tomato crop, 10 hectres", driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
