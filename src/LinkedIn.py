from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import random
from bs4 import BeautifulSoup

#
#  CLEAN UP THIS CODE MOFO'S
#

# Login Error
#
# Description: This exception handles an Agent error if there is an error in logging into the site

class LoginError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# class:
class LinkedIn:
    def __init__(self, username, password, phone, server_db, driver, display, database_array):

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
        self.database_array = database_array

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
        password_form.send_keys(Keys.RETURN)

        # sleep for 3 seconds
        time.sleep(3)

        # validate login
        try:
            disposable_variable = self.driver.find_elements_by_class_name('name')
        except NoSuchElementException as e:
            raise LoginError("Could not Login to Linkedin")


    def __get_profile_information(self, url_sent, Term):

        # set parameters
        name_form = None
        discription_form = None
        location_form = None
        current_form = None
        background_experience = None

        education_form = []
        experience_array = []
        # relevant pieces of information

        person_dictionary = dict()

        # name
        try:
            name_form = self.driver.find_element_by_class_name('full-name')
        except:
            # cannot find element
            pass

        # discription
        try:
            discription_form = self.driver.find_element_by_id('headline')
        except:
            # do stuff
            pass

        # locality
        try:
            location_form = self.driver.find_element_by_class_name('locality')
        except:
            # do stuff
            pass

        # current work
        try:
            current_form = self.driver.find_element_by_id('overview-summary-current')
        except:
            # do stuff
            pass

        # current work
        try:
            current_form = self.driver.find_element_by_id('background-education')
            educationSoup = BeautifulSoup(current_form.get_attribute('innerHTML'), 'html.parser')
            for link in educationSoup.find_all('div', class_='education'):
                educationDict = dict()
                try:
                    educationLink = link.find("header")
                    try:
                        educationDict['school'] = educationLink.find("h4").get_text()
                        try:
                            more_processing = educationLink.find("h5")
                            try:
                                educationDict['degree'] = more_processing.find('span', class_="degree").get_text()
                                educationDict['major'] = more_processing.find('span', class_="major").get_text()
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
                education_form.append(educationDict);
        except:
            # do stuff
            pass

        # current work
        try:
            background_experience = self.driver.find_element_by_id('background-experience')
            experienceSoup = BeautifulSoup(background_experience.get_attribute('innerHTML'), 'html.parser')
            for link in experienceSoup.find_all('div', class_='editable-item'):

                the_dictionary = dict()

                temp_titleJob = None
                temp_companyJob = None
                temp_timeExperienceJob = None
                temp_summaryJob = None

                try:
                    temp_titleJob = link.find('h4').get_text()
                    the_dictionary['job'] = temp_titleJob
                except:
                    pass

                try:
                    temp_companyJob = link.find('h5').get_text()
                    the_dictionary['company'] = temp_companyJob
                except:
                    pass

                try:
                    temp_timeExperienceJob = link.find('span', class_='experience-date-locale').get_text()
                    the_dictionary['experience'] = temp_timeExperienceJob
                except:
                    pass

                try:
                    temp_summaryJob = link.find('p', class_='summary-field-show-more').get_text()
                    the_dictionary['summary'] = temp_summaryJob
                except:
                    pass

                experience_array.append(the_dictionary)

        except:
            # do stuff
            pass

        if name_form != None:
            print(name_form.text)
            person_dictionary['name'] = name_form.text
            person_dictionary['url'] = url_sent
            person_dictionary['searchTerm'] = Term

        if discription_form != None:
            print(discription_form.text)
            person_dictionary['discription'] = discription_form.text

        if location_form != None:
            print(location_form.text)
            person_dictionary['location'] = location_form.text

        if current_form != None:
            print(current_form.text)
            person_dictionary['currentJob'] = current_form.text

        if experience_array:
            print(experience_array)
            person_dictionary['experiences'] = experience_array

        if education_form:
            print(education_form)
            person_dictionary['education'] = education_form

        # push to database
        if person_dictionary:
            result = self.db.LinkedinUsers.insert_one(person_dictionary)
            print(result.inserted_id)

        # figure out a proper wait time for linkedin
        WaitTime = random.randint(4, 10)
        time.sleep(WaitTime)
        return

    def search(self, Term, Limit, Database_save=True, Recursive=True, Recursion=3):
        searchBar = self.driver.find_element_by_id('main-search-box')

        # clear the bars
        searchBar.clear()
        searchBar.send_keys(Term)

        # Sleep before sending info
        time.sleep(int(len(Term) / 3))

        # Press enter
        searchBar.send_keys(Keys.RETURN)

        time.sleep(3)
        set_urls = []

        total_urls = []

        while Limit > len(set_urls):
            time.sleep(3)
            # find more people
            elements = self.driver.find_elements_by_class_name("people")
            for element in elements:
                try:
                    attributeHere = element.find_element_by_class_name("result-image");
                    link = attributeHere.get_attribute("href")
                    if "profile" in link:
                        newPersonUrl = link.split("&auth")[0]
                        set_urls.append(newPersonUrl)
                        print(newPersonUrl)
                except:
                    pass

            # check if we have exceeded our search limit
            if len(set_urls) < 5:
                break

            print(set_urls)

            time.sleep(3)
            # go to next page
            pagination = self.driver.find_elements_by_class_name("pagination")
            for pages in pagination:
                click_next = pages.find_element_by_class_name("next")
                click_next.click()
                break

        total_urls += set_urls

        # get more
        main_window = self.driver.current_window_handle

        index_recursion = 0
        while Recursion > index_recursion:
            new_list = set_urls[:]
            print(set_urls)
            set_urls = []
            for each_url in new_list:
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
                time.sleep(2)
                self.driver.switch_to.window(main_window)
                self.driver.get(each_url)
                time.sleep(2)
                # do something recursive
                recommended = self.driver.find_elements_by_class_name("browse-map-photo")
                for person in recommended:
                    try:
                        personLink = person.get_attribute("href")
                        if "profile" in personLink:
                            set_urls.append(personLink)
                    except:
                        pass
                time.sleep(3)
                similar = self.driver.find_elements_by_class_name("discovery-photo")
                for person in similar:
                    try:
                        personLink = person.get_attribute("href")
                        if "profile" in personLink:
                            newPersonUrl = personLink.split("&auth")[0]

                            # check for duplicates
                            if not (newPersonUrl in set_urls) and not (newPersonUrl in total_urls):
                                set_urls.append(newPersonUrl)
                    except:
                        pass

                # get info of person
                if Database_save:
                    self.__get_profile_information(each_url, Term)
                # here get the info end

                time.sleep(2)
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
                time.sleep(2)
                self.driver.switch_to.window(main_window)
                print(len(set_urls))
            total_urls += set_urls
            index_recursion = index_recursion + 1
        return total_urls
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