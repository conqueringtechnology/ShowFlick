# Unit test file to determine if the Shows & Movies page is displayed when the user
# clicks the 'Shows & Movies' button in the navigation pane of the ShowFlow app
# Shows & Movies page is shown if the 'Search' button exists on the page
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


# Shows & Movies is shown if the 'Search' button exists on the page
    def test_ll(self):
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)  # pause to allow screen to load
    # click the login button - user must be logged in to view the Customer list
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[2]/li/a').click()
# find the username and password input boxes and login
        user = "testuser"  # must be a valid username for the application
        pwd = "test123"  # must be the password for a valid user
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)  # pause to allow screen to load
# find 'Shows & Movies in Nav Bar' and click it – note this is all one Python statement
        elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[1]/li[4]/a').click()
        time.sleep(3)  # pause to allow screen to change
        try:
# verify 'Search' button exists on new screen after clicking "Shows & Movies nav link"
            elem = driver.find_element(By.XPATH, '/html/body/div[5]/form/div[2]/button')
            print("Test passed - Product Information displayed")
            assert True
        except NoSuchElementException:
         self.fail("Shows & Movies Page does not appear when Shows & Movies nav link is clicked - test failed")


def tearDown(self):
    self.driver.close()


if __name__ == "__main__":
    unittest.main()
