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

        # start instance of browser
        self.driver.get("http://www.linkedin.com")

        # sleep for 6 seconds
        time.sleep(6)

        # login to linkedin
        # send login keystrokes
        login_form = self.driver.find_element_by_id('login-email')
        login_form.send_keys(self.username)

        # sleep for 3 seconds
        time.sleep(3)

        # send password keystrokes
        password_form = self.driver.find_element_by_id('login-password')
        password_form.send_keys(self.password)

        # sleep for 3 seconds
        time.sleep(3)

        # hit enter key in password form
        password_form.send_keys(Keys.RETURN);

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('name')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Linkedin")

        # login worked
        return True

    def search(self):
        pass

    def post(self):
        pass

    def message(self):
        pass

    def close(self):
        # go to the homepage
        self.driver.get("https://www.linkedin.com")

        # open the account settings
        element = self.driver.find_element_by_class_name("account-settings-tab")
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()

        # press sign out on the menu
        menu_elements = self.driver.find_elements_by_class_name('account-submenu-split-link')
        for element in menu_elements:
            if "Sign Out" in element.text:
                element.click()
                break

        # sleep for 3000 seconds
        time.sleep(3)

        #close function
        return