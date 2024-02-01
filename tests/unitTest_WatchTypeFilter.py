# Unit test file to determine if the Movie type Filter brings up the Movie types
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import warnings


class ll_ATS(unittest.TestCase):


# set up the test class - assign the driver to Chrome - if using a different


# browser, change the browser name below
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning)  # ignore resource warning if occurs
# Test if Customer list is displayed when Customers is clicked in the Navigation bar


# Watch Type Filter is functional if Streaming colum = Movie
    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)  # pause to allow screen to load
    # click the login button - user must be logged in to view the Customer list
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[2]/li[1]/a').click()
# find the username and password input boxes and login
        user = "testuser"  # must be a valid username for the application
        pwd = "test123"  # must be the password for a valid user
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)  # pause to allow screen to load
# find Shows & Movies Nav link and click on it
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[1]/li[4]/a').click()
        time.sleep(3)  # pause to allow screen to change
        #find filter drop down and click on it
        elem = driver.find_element(By.XPATH, '//*[@id="id_watch_type"]').click()
        # select movie type
        type = "Movie"
        elem = driver.find_element(By.ID, "id_watch_type")
        elem.send_keys(type)
        # find Search button and click on it
        elem = driver.find_element(By.XPATH, '/html/body/div[6]/form/div[3]/button').click()
        try:
# verify Movie type displays
            elem = driver.find_element(By.XPATH, '//*[@id="userlist"]/table/tbody/tr[2]/td[9]')
            print("Test passed- Type Movie is displayed")
            assert True
        except NoSuchElementException:
         self.fail("Type Movie not displayed - test failed")


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()