from enum import Enum
from connection import Connection
from LinkedIn import LinkedIn
from Google import Google
from Twitter import Twitter

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
#   Firefox
#   Chrome
#

class Sites(Enum):
    LinkedIn = 1
    Google = 2
    Twitter = 3


# class: Bot
#
# Description: This is a class that allows someone to connect to a mongo server and do all the
#              necessary functions.
#
# Methods:
#
#       insert: insert data into the selected database and collection
#       get_data: get data from the selected database and collection
#

class Bot:
    def __init__(self, username, password, phone, site=Sites.LinkedIn, UserInterface=UserAgent.Firefox, database_url=None, databases_array=None):

        # Check the Agent and if it matches the Enum type
        if not isinstance(UserInterface, UserAgent):
            raise AgentError('Please select the correct UserAgent:  Types: [Firefox] [Chrome]')

        # Check the Site and if it matches the Enum type
        if not isinstance(site, Sites):
            raise SiteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')

        # Variables for the login
        self.username = username
        self.password = password
        self.phone = phone
        self.user_interface = UserInterface

        self.site = None
        self.server = None

        # Check if the database is being used
        if database_url and databases_array:
            self.server = Connection(database_url, databases_array)

        # Get the correct object for the sites
        if site.name == "Google":
            self.site = Google()
        elif site.name == "LinkedIn":
            self.site = LinkedIn()
        elif site.name == "Twitter":
            self.site = Twitter()

        raise SiteError('Please select the correct site:  Types: [Google] [LinkedIn] [Twitter]')