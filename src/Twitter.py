from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

# class:
class Twitter:
    def __init__(self, username, password, phone, server_db, driver, display):

        #
        # Section 4:    Database Setup
        #
        # Description:  This section is there to setup a database connection to push data to the database
        #

        self.username = username
        self.password = password
        self.phone = phone
        self.database = server_db
        self.browser = driver
        self.display = display


        pass

    def hello(self):
        print("yeah")