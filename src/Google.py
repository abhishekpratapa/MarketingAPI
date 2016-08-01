from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import datetime
import random

# Login Error
#
# Description: This exception handles an Agent error if there is an error in logging into the site

class LoginError(Exception):
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

    def search(self,query_term,search_limit,start_date,end_date,location):

        #
        # Section 1:    Search Bar
        #
        # Description:  This section is to identify the search bar and query it
        #

        # search bar identification
        searchBar = self.driver.find_element_by_id("lst-ib")

        # clear the bars
        searchBar.clear()
        searchBar.send_keys(query_term)
        searchBar.send_keys(Keys.RETURN)

        # Sleep before sending info
        time.sleep(int(len(query_term) / 3))

        # Press enter
        searchBar.send_keys(Keys.RETURN)

        #
        # Section 2:    Date Section
        #
        # Description:  This section is put in a date to the search fields to allow searching via date
        #

        # this scenario is if both the start dates and the end dates were given
        if not (start_date == "0/0/0" and end_date == "0/0/0"):

            # click on the more button
            more_button = self.driver.find_element_by_id("hdtb-tls")
            more_button.click()

            # sleep for 3 seconds
            time.sleep(3)

            # select an option to chose date range
            range_selector = self.driver.find_elements_by_class_name("mn-hd-txt")

            for select in range_selector:
                if ("Any time" in select.get_attribute("innerHTML")):
                    select.click()
                    break

            # sleep for 3 seconds
            time.sleep(3)

            # click on the calander link
            click_calandar_link = self.driver.find_element_by_id("cdrlnk")
            click_calandar_link.click()

            # sleep for 3 seconds
            time.sleep(3)

            # find the start date selection
            cdr_min = self.driver.find_element_by_id("cdr_min")
            cdr_min.send_keys(start_date)

            # sleep for 3 seconds
            time.sleep(3)

            # find the end date selection
            cdr_max = self.driver.find_element_by_id("cdr_max")
            cdr_max.send_keys(end_date)

            # submit the date
            index_date = 0

            submit_date = self.driver.find_elements_by_class_name("ksb")
            for sub in submit_date:
                index_date = index_date + 1
                if ("ksb mini cdr_go" in sub.get_attribute("class")) and index_date == 2:
                    print(sub.get_attribute("value"))
                    sub.click()
                    break

            # sleep for 3 seconds
            time.sleep(3)

        # this section is if only a start date is provides and it adds one month to capture the end date
        elif not (start_date == "0/0/0"):

            # click on the more button
            more_button = self.driver.find_element_by_id("hdtb-tls")
            more_button.click()

            # sleep for 3 seconds
            time.sleep(3)

            # select an option to chose date range
            range_selector = self.driver.find_elements_by_class_name("mn-hd-txt")

            for select in range_selector:
                if ("Any time" in select.get_attribute("innerHTML")):
                    select.click()
                    break

            # sleep for 3 seconds
            time.sleep(3)

            # click on the calander link
            click_calandar_link = self.driver.find_element_by_id("cdrlnk")
            click_calandar_link.click()

            # sleep for 3 seconds
            time.sleep(3)

            # find the start date selection
            cdr_min = self.driver.find_element_by_id("cdr_min")
            cdr_min.send_keys(start_date)

            # add one month to the start date
            dt = datetime.datetime.strptime(start_date, '%m/%d/%Y')
            newTimestamp = time.mktime(dt.timetuple())
            nextMonth = int(newTimestamp) + 2721600;
            newDate = datetime.datetime.fromtimestamp(nextMonth).strftime("%m/%d/%Y")

            # put in the new end date
            cdr_max = self.driver.find_element_by_id("cdr_max")
            cdr_max.send_keys(newDate)

            # submit the date
            index_date = 0

            submit_date = self.driver.find_elements_by_class_name("ksb")
            for sub in submit_date:
                index_date = index_date + 1
                if ("ksb mini cdr_go" in sub.get_attribute("class")) and index_date == 2:
                    print(sub.get_attribute("value"))
                    sub.click()
                    break

            # sleep for 3 seconds
            time.sleep(3)

        #
        # Section 3:    Searches
        #
        # Description:  Actually go through the search terms
        #

        # find all class "r" terms
        main_window = self.driver.current_window_handle
        searchArray = []

        # sleep for 10 seconds
        time.sleep(10)


        # check if we have reached the limit for search terms
        while search_limit > len(searchArray):

            # sleep for 5 seconds
            time.sleep(5)

            # select the search links
            new_elements = self.driver.find_elements_by_xpath("//h3[contains(@class,'r')]/a")

            # check how many elements are on that page
            looper = len(new_elements) - 1
            indexLoop = 0;

            # loop through all search terms on the page
            while looper > indexLoop:

                # try to get the url of the link
                try:

                    # find the link in the elements
                    elements_with_r = self.driver.find_elements_by_xpath("//h3[contains(@class,'r')]/a")

                    # list the title
                    print(elements_with_r[indexLoop].get_attribute("innerHTML"))

                    # open the url in a new tab
                    elements_with_r[indexLoop].send_keys(Keys.COMMAND + Keys.RETURN)

                    # sleep for 1 seconds
                    time.sleep(1)

                    # switch to the new tab
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

                    # sleep from 4 to 7 seconds
                    time.sleep(random.randint(4, 7))

                    # put the url into the search array
                    searchArray.append(self.driver.current_url)

                    # switch to the current window to send commands to the new tab
                    self.driver.switch_to.window(main_window)

                    # sleep for 2 seconds
                    time.sleep(2)

                    # close the current window
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')

                    # sleep from 4 to 7 seconds
                    time.sleep(random.randint(4, 7))

                    # switch to the current window to send commands to main google search
                    self.driver.switch_to.window(main_window)
                except:

                    # sleep from 4 to 7 seconds
                    time.sleep(random.randint(4, 7))

                    # pass since we failed
                    pass

                # check if the search query limit has been reached
                if search_limit < len(searchArray):

                    # exit loop
                    break

                # add to the index to go to the next search term
                indexLoop = indexLoop + 1

            # print the whole array every page
            print(searchArray)

            # sleep for 4 seconds
            time.sleep(4)

            # click the next button to go to the next page
            backbutton = self.driver.find_elements_by_class_name('pn')
            backbutton[len(backbutton) - 1].click()

            # sleep for 3 seconds
            time.sleep(3)

        # end of the loop

        # sleep for 4 seconds
        time.sleep(4)

        # return the array with the specified length
        return searchArray[:search_limit]

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