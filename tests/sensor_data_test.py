import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import env
import warnings



class SensorDataTest(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def test_sensor_data_page(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.driver.get(f"{env.host}/login")
        self.driver.implicitly_wait(0.5)
        self.assertIn("Index Insurance", self.driver.title)
        elem = self.driver.find_element(By.NAME, "passphrase")
        elem.send_keys(env.account_two_memonic)
        elem.send_keys(Keys.RETURN)
        join_policy = self.driver.find_element(By.ID, "sensordata")
        join_policy.click()
        self.driver.implicitly_wait(5)
        # driver.execute_script("return jQuery.active == 0")
        self.assertIn("Sensor Data", self.driver.page_source)
        self.assertIn(env.account_two_address, self.driver.page_source)

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()

