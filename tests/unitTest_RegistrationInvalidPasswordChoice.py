# Selenium test script
# test script to verify an all numeric password cannot be chosen at registration.
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import warnings


class ll_ATS(unittest.TestCase):
    # set up the test class - assign the driver to Chrome - if using a different
    # browser, change the browser name below
    def setUp(self):
        self.driver = webdriver.Chrome()
        warnings.simplefilter('ignore', ResourceWarning)  # ignore resource warning if occurs

    # If login is successful, 'Logout' will be displayed as the text in the Navbar
    def test_ll(self):
        user = "testuserpassword"  # must be a valid username for the application
        pwd1 = "123456789"
        pwd2 = "123456789"
        fname = "test"
        lname = "user"
        email = "testuserpassword@email.com"
        # open the browser and go to the admin page
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/register")
        # find the username and password input boxes on the screen by ID
        # send the username and password to each box
        # send the Return (Enter) key to the system
        # go to the main application page
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password1")
        elem.send_keys(pwd1)
        elem = driver.find_element(By.ID, "id_password2")
        elem.send_keys(pwd2)
        elem = driver.find_element(By.ID, "id_first_name")
        elem.send_keys(fname)
        elem = driver.find_element(By.ID, "id_last_name")
        elem.send_keys(lname)
        elem = driver.find_element(By.ID, "id_email")
        elem.send_keys(email)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.get("http://127.0.0.1:8000")
        time.sleep(3)
        # pause to let screen change
        time.sleep(3)
        # Register link is shows, meaning registation did not validate
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="myNavbar"]/ul[2]/li[2]/a')
            print("Test Passed - Invalid password rule enforced")
            assert True
        # else report that the test failed
        except NoSuchElementException:
            self.fail("Test Failed - password rule not enforced")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
