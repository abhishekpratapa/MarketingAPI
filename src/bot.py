from enum import Enum
from connection import Connection
from LinkedIn import LinkedIn
from Google import Google
from Twitter import Twitter
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random


# Agent Error
#
# Description: This exception handles an Agent error if the variable is the wrong Agent or Type

class AgentError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Site Error
#
# Description: This exception handles an Site error if the variable is the wrong Site or Type

class SiteError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Enumerated Type: User Agent
#
#   Description:  This is a User Agent enumerated type.
#                 It is used to select the browser to use in the bot agent.
#
# Options:
#
#   Firefox
#   Chrome
#

class UserAgent(Enum):
    Firefox = 1
    Chrome = 2


# Enumerated Type: Sites
#
#   Description:  This is a Sites enumerated type.
#                 This is used to select the site to use in the bot agent.
#
# Options:
#
#   LinkedIn
#   Google
#   Twitter
#

class Sites(Enum):
    LinkedIn = 1
    Google = 2
    Twitter = 3


# class: Bot
#
# Description: This is a class that allows to create a new marketing bot to scrape information
#              and allows the user to go through and post data on relevant sites
#
# Methods:
#
#       search:     Search the relevant User Agent for information
#       post:       Post public messages to the relevant social media websites
#       message:    Send a private message to anyone within that network
#       close:      Close the current web browser

class Bot:
    def __init__(self, username, password, phone, site=Sites.LinkedIn, UserInterface=UserAgent.Firefox, display=False, database_url=None, databases_array=None):

        #
        # Section 1:    Error Checking
        #
        # Description:  This section is pertinent to error checking for the constructor
        #

        # Check the Agent and if it matches the Enum type
        if not isinstance(UserInterface, UserAgent):
            raise AgentError('Please select the correct UserAgent:  Types: [Firefox] [Chrome]')

        # Check the Site and if it matches the Enum type
        if not isinstance(site, Sites):
            raise SiteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

        #
        # Section 2:    Display
        #
        # Description:  Check whether its a headless browser and if so create a virtual display
        #

        self.display = None

        # check whether the display is on or off
        if not display:
            self.display = Display(visible=False, size=(1980, 1024))
            self.display.start()

        # open the proper interface
        if UserInterface.name == "Firefox":
            self.driver = webdriver.Firefox()
        elif UserInterface.name == "Chrome":
            self.driver = webdriver.Chrome()
        else:
            raise NameError('The specified useragent doesn\'t exist')

        #
        # Section 3:    Variables
        #
        # Description:  This section holds the major variables for the Bot Class
        #

        # Variables for the login
        self.username = username
        self.password = password
        self.phone = phone
        self.database_array = databases_array
        #
        # Section 4:    Database Setup
        #
        # Description:  This section is there to setup a database connection to push data to the database
        #

        self.server_db = None

        # Check if the database is being used
        if database_url and databases_array:
            self.server_db = Connection(database_url, databases_array)

        #
        # Section 5:    Agent Setup
        #
        # Description:  This section setups the agent for all of the websites
        #

        self.siteAgent = None

        # Get the correct object for the sites
        if site.name == "Google":
            self.siteAgent = Google(self.username, self.password, self.phone, self.server_db, self.driver, self.display, self.database_array)
        elif site.name == "LinkedIn":
            self.siteAgent = LinkedIn(self.username, self.password, self.phone, self.server_db, self.driver, self.display, self.database_array)
        elif site.name == "Twitter":
            self.siteAgent = Twitter(self.username, self.password, self.phone, self.server_db, self.driver, self.display, self.database_array)
        else:
            raise SiteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')


    # method: search
    #
    # Description: This method goes through
    #
    # parameter
    #
    # return:

    def search(self, array_keywords, search_limit=100, addendums=None,start_date="0/0/0", end_date="0/0/0", index_database=0, collection_name=None,website=None):

        # Select an append to the search query
        add_choice = ""

        # Loop through the keywords to search
        for key in array_keywords:
            # Check if there are additions to the search query
            if addendums:
                add_choice = " "+random.choice(addendums)

            # full query term
            query_term = str(key)+str(add_choice)

            # search the key's
            self.siteAgent.search(query_term,search_limit,start_date,end_date,index_database,collection_name,website)

        #close the
        return

    def post(self, message):

        # post a message hello
        self.siteAgent.post(message)

        # close function
        return

    def message(self, person_tag, subject, message):

        # a call to the messaging method call
        self.siteAgent.message(person_tag, subject, message)

        # close function
        return

    def close(self):

        # logout of agent
        self.siteAgent.close()

        # close the browser
        self.driver.close()

        # close function
        return