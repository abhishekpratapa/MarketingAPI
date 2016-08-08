#### Facebook Web Crawler
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import random
from bs4 import BeautifulSoup
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
class Facebook:
    def __init__(self, username, password, phone, server_db, driver, display, database_array):

        #
        # Section 1:    Variables Section
        #
        # Description:  This section holds the major variables for the Bot Class
        #

        self.username = username
        self.password = password
        self.phone = phone
        self.database = server_db
        self.driver = driver
        self.display = display
        self.database_array = database_array

        #
        # Section 2:    Setup Secton
        #
        # Description:  This section setups everything needed for the other functions
        #

        # start instance of browser
        self.driver.get("http://www.facebook.com")

        # sleep for 6 seconds
        time.sleep(6)

        # login to Facebook
        # send login keystrokes
        login_form = self.driver.find_element_by_id('email')
        login_form.send_keys(self.username)

        # sleep for 3 seconds
        time.sleep(3)

        # send password keystrokes
        password_form = self.driver.find_element_by_id('pass')
        password_form.send_keys(self.password)

        # sleep for 3 seconds
        time.sleep(3)

        # hit enter key in password form
        password_form.send_keys(Keys.RETURN);

        temporary = input('Wait for Input')

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_element_by_class_name('_4kny')

        except NoSuchElementException as e:
            raise LoginError("Could not Login to Facebook")

        # login worked
        return

    def find_groups(self, keywords):
        # enter search term
        search_form = self.driver.find_element_by_class_name('_1frb')
        search_form.send_keys(keywords)
        time.sleep(3)
        search_form.send_keys(Keys.RETURN)
        time.sleep(8)


        # Navigate to Group Tab
        tabs = self.driver.find_elements_by_class_name('_5vwz')
        numtabs = len(tabs)
        self.driver.implicitly_wait(3)

        # Must Strucuture Loop this way to avoid StaleElement
        # as opposed to simply [for cats in tabs:]
        for i in range(numtabs):
            cats = self.driver.find_elements_by_class_name('_5vwz') # recall to avoid StaleElementError
            if 'Group' in BeautifulSoup(cats[i].get_attribute('innerHTML'),'html.parser').a.div.text:
                cats[i].click()
            else:
                time.sleep(1)

        time.sleep(4)

        # Collect All the Groups and Filter by Open / Closed
        groups = self.driver.find_elements_by_class_name('_glj')
        numgroups = len(groups)


        for i in range(numgroups):
            # Refresh Group every loop to avoid Stale Element Error
            group = self.driver.find_elements_by_class_name('_glj')
            group_name = self.driver.find_elements_by_class_name('_gll')
            soup = BeautifulSoup(group[i].get_attribute('innerHTML'), 'html.parser')
            group_type = soup.find('div',{'class':'_pac'})

            # If public go through and scrape members of group
            if 'Public' in group_type.text:
                # Create DB for group
                public_group = dict()

                # Record Group Name
                gname_soup = BeautifulSoup(group_name[i].get_attribute('innerHTML'),'html.parser')

                # Navigate to Group Page
                group[i].find_element_by_class_name('_gll').find_element_by_tag_name('a').click()
                print ('clicked on open group {}'.format(gname_soup.text))
                public_group['Name'] = gname_soup.text
                public_group['Group Name'] = gname_soup.text
                time.sleep(random.randint(1, 3))
                members = self.driver.find_element_by_class_name('_5dw8')

                # Navigate to list of Members
                members.find_element_by_tag_name('a').click()

                # Scrape Member Names and Work
                # This is the container that holds the member info
                containers = self.driver.find_elements_by_class_name('_6a')

                # loop through and pull name and work
                people = []  # hold list of member names
                for form in containers:
                    if ('_6a _5u5j _6b' in form.get_attribute('class')):
                        # Dictionary to store member info
                        member = dict()
                        # Finding Name & Bios
                        name = form.find_element_by_class_name('fsl')
                        work = form.find_element_by_class_name('_17tq')
                        soup_name = BeautifulSoup(name.get_attribute('innerHTML'),'html.parser')
                        soup_work = BeautifulSoup(work.get_attribute('innerHTML'), 'html.parser')
                        print('NAME: {}'.format(soup_name.text))
                        member['Name'] = (soup_name.text)
                        print('WORK: {}'.format(soup_work.text))
                        member['Bio'] = (soup_work.text)
                        people.append(member)
                # Store Members in Group Dictionary
                public_group['Memebers'] = people
                print ('*** END OF GROUP ***')

                # Navigate Back to Page With List of Groups
                self.driver.back()  # moves back to group page
                time.sleep(random.randint(1, 4))
                self.driver.back()  # back to list of groups page
                time.sleep(random.randint(1, 4))
            else:
                pass

    def lvl1_friends(self):

        pass

    def search(self,search):
        pass

    def post(self):
        pass

    def message(self):
        pass

    def close(self):
        # go to the homepage
        self.driver.get("https://www.facebook.com")

        # open the account settings
        element = self.driver.find_element_by_class_name("pass")
        hov = ActionChains(self.driver).move_to_element(element)
        hov.perform()

        #Successful Logout
        return