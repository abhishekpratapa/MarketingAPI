from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time


# Login Error
#
# Description: This exception handles an Agent error if there is an error in logging into the site

class LoginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# class:
class Google:
    def __init__(self, username, password, phone, server_db, driver, display):

        #
        # Section 1:    Variables Secton
        #
        # Description:  This section holds the major variables for the Bot Class
        #

        self.username = username
        self.password = password
        self.phone = phone
        self.database = server_db
        self.driver = driver
        self.display = display

        #
        # Section 2:    Setup Secton
        #
        # Description:  This section setups everything needed for the other functions
        #

        # login to Google
        self.driver.get("http://www.google.com")

        # sleep for 3 seconds
        time.sleep(3)

        # Initiate login sequence
        # Click sign in button
        login_button = self.driver.find_element_by_id("gb_70")
        login_button.click()

        # sleep for 6 seconds
        time.sleep(6)

        # send my email address
        login_form_gmail = self.driver.find_element_by_id('Email')
        login_form_gmail.send_keys(self.username)

        # sleep for 5 seconds
        time.sleep(5)

        # Hit the return key to continue
        login_form_gmail.send_keys(Keys.RETURN)

        # sleep for 3 seconds
        time.sleep(3)

        # type in the password
        password_form_gmail = self.driver.find_element_by_id('Passwd')
        password_form_gmail.send_keys(self.password)

        # sleep for 5 seconds
        time.sleep(5)

        # Hit the return key to complete logging in
        password_form_gmail.send_keys(Keys.RETURN)

        # sleep for 5 seconds
        time.sleep(5)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('tsf')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Google")

    def search(self):
        pass

    def post(self):
        pass

    def message(self):
        pass

    def close(self):
        # go to the homepage
        self.driver.get("https://accounts.google.com/SignOutOptions?hl=en&continue=https://www.google.com/")

        # sleep for 3 seconds
        time.sleep(3)

        # Click log out button
        logout_button = self.driver.find_element_by_id("signout")
        logout_button.click()

        #close function
        return