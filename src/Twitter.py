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
class Twitter:
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

        # go to twitter.com
        self.driver.get("http://twitter.com")

        # sleep for 6 seconds
        time.sleep(6)

        # test if the sign-up button was successfully pressed
        login_button = None

        # login to Twitter
        try:
            # press the Login Button
            login_button = self.driver.find_element_by_class_name("js-login")
            print("Success")
        except:
            login_button = self.driver.find_element_by_id("signin-link")

        # press the login button
        login_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # send email address
        email_text = self.driver.find_element_by_name("session[username_or_email]")
        email_text.send_keys(self.username)

        # sleep for 3 seconds
        time.sleep(3)

        # send password keystrokes
        password_text = self.driver.find_element_by_name("session[password]")
        password_text.send_keys(self.password)

        # sleep for 3 seconds
        time.sleep(3)

        # hit enter key in password form
        password_text.send_keys(Keys.RETURN)

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('DashboardProfileCard-avatarImage')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Twitter")

    def search(self):
        pass

    def post(self):
        pass

    def message(self):
        pass

    def close(self):
        # go to the homepage
        self.driver.get("https://www.twitter.com/")

        # sleep for 3 seconds
        time.sleep(3)

        # Click profile button
        toggle_button = self.driver.find_element_by_id("user-dropdown-toggle")
        toggle_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # Click logout button
        logout_button = self.driver.find_element_by_id("signout-button")
        logout_button.click()

        # sleep for 3 seconds
        time.sleep(3)

        # close function
        return