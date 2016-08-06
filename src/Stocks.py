import os
import pprint
import json
import time
import bot
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import re
import calendar
import requests
from collections import deque
from pymongo import MongoClient
from threading import Thread
from datetime import timedelta, date


#def for dates
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Method: stocks_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
# parameter catagory [String]:          this parameter is a catagory string
# parameter catagory_number [String]:   this parameter is a catagory number
#
# return: the dictionary element of the data

def stocks_dictionary(ticker, name, exchange, catagory, catagory_number):
    stock_element = dict()
    stock_element['ticker'] = ticker
    stock_element['name'] = name
    stock_element['exchange'] = exchange
    stock_element['catagory'] = catagory
    stock_element['catagory_number'] = catagory_number
    stock_element['type'] = "stocks"
    return stock_element


# Method: currency_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the currency dictionary of the data

def currency_dictionary(ticker, name, exchange):
    currency_element = dict()
    currency_element['ticker'] = ticker
    currency_element['name'] = name
    currency_element['exchange'] = exchange
    currency_element['type'] = "currency"
    return currency_element


#  Method: etf_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the etf dictionary of the data

def etf_dictionary(ticker, name, exchange):
    etf_element = dict()
    etf_element['ticker'] = ticker
    etf_element['name'] = name
    etf_element['exchange'] = exchange
    etf_element['type'] = "etf"
    return etf_element


#  Method: future_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the future dictionary of the data

def future_dictionary(ticker, name, exchange):
    future_element = dict()
    future_element['ticker'] = ticker
    future_element['name'] = name
    future_element['exchange'] = exchange
    future_element['type'] = "future"
    return future_element


#  Method: index_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the index dictionary of the data

def index_dictionary(ticker, name, exchange):
    index_element = dict()
    index_element['ticker'] = ticker
    index_element['name'] = name
    index_element['exchange'] = exchange
    index_element['type'] = "index"
    return index_element


#  Method: mutual_fund_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the mutual fund dictionary of the data

def mutual_fund_dictionary(ticker, name, exchange):
    mutual_fund_element = dict()
    mutual_fund_element['ticker'] = ticker
    mutual_fund_element['name'] = name
    mutual_fund_element['exchange'] = exchange
    mutual_fund_element['type'] = "mutual"
    return mutual_fund_element


#  Method: bonds_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the bond dictionary of the data

def bonds_dictionary(ticker, name, exchange):
    bonds_element = dict()
    bonds_element['ticker'] = ticker
    bonds_element['name'] = name
    bonds_element['exchange'] = exchange
    bonds_element['type'] = "bonds"
    return bonds_element

#  Method: warrant_dictionary
#
# Description: insert data into the Mongo database
#
# parameter ticker [String]:            this parameter is a ticker string
# parameter name [String]:              this parameter is a name string
# parameter exchange [String]:          this parameter is an exchange string
#
# return: the warrant dictionary of the data

def warrant_dictionary(ticker, name, exchange):
    warrant_element = dict()
    warrant_element['ticker'] = ticker
    warrant_element['name'] = name
    warrant_element['exchange'] = exchange
    warrant_element['type'] = "warrant"
    return warrant_element

# class: Stocks
#
# Description: This is a class that allows to create a new stock bot
#
# Methods:
#

class Stocks:
    def __init__(self, terminal=True):
        # the current window is set to the main window
        self.current_window = 0

        self.client = MongoClient("mongodb://127.0.0.1:27017")
        self.db = self.client.Stock_Agent

        # fill this with potential array hits
        self.current_prospects = []

        self.function_definitions = {
            3: stocks_dictionary,
            4: bonds_dictionary,
            5: currency_dictionary,
            6: etf_dictionary,
            7: future_dictionary,
            8: index_dictionary,
            9: mutual_fund_dictionary,
            10: warrant_dictionary
        }

        self.files = {
            3: "stock_data/Stock.json",
            4: "bonds_data/Bond.json",
            5: "currency_data/Currency.json",
            6: "etf_data/ETF.json",
            7: "future_data/Future.json",
            8: "index_data/index.json",
            9: "mutual_fund_data/MutualFund.json",
            10: "warrant_data/Warrant.json"
        }


        # check if the user wants terminal access
        if terminal:
            self.terminal()

    # This part of the program takes care of the user inputs
    def terminal(self):
        # Loop the program
        while True:

            # Clear the screen and display the relevant information
            os.system('cls' if os.name == 'nt' else 'clear')
            self.display_options(self.current_window)

            # Select what to do next
            selection = input('Please Choose a selection: ')
            result_page = self.return_relevant_page(self.current_window, int(selection))

            if result_page < 0:
                # Exit program
                if result_page == -1:
                    exit()

                self.display_apporiate_data((result_page*-1), self.current_window)
                continue

            self.current_window = result_page

    def scrape_articles(self, website):

        pass

    def display_options(self, index=0):

        options = [
            "MAIN WINDOW\n\n[1] Display Info\n[2] Take Action\n\n[3] Exit",
            "DISPLAY INFO\n\n[1] Stocks\n[2] Bonds\n[3] Currency\n[4] ETF\n[5] Future\n[6] Index\n[7] Mutual Fund\n[8] Warrant\n\n[9] Back",
            "TAKE ACTION\n\n[1] Scrape\n[2] Learn\n[3] Trade\n\n[4] Back",
            "STOCKS\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "BONDS\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "CURRENCY\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "ETF\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "FUTURE\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "INDEX\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "MUTUAL FUND\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "WARRANT\n\n[1] Display All\n[2] Search\n[3] Add to Prospective\n\n[4] Back",
            "SCRAPE\n\n[1] Scrape Google for email Addresses\n[2] Scrape LinkedIn for profiles relating to the company\n\n[3] Back",
            "LEARN\n\n[1] Learn from Articles on CNN.com\n\n[2] Back",
            "TRADE\n\n[1] Automatically Trade the Stocks\n\n[2] Back"
        ]

        print(options[index])

    def return_relevant_page(self, current_page, input):

        pages = {
            0: "main",
            1: "display",
            2: "actions",
            3: "stocks",
            4: "bonds",
            5: "currency",
            6: "etf",
            7: "future",
            8: "index",
            9: "mutual",
            10: "warrant",
            11: "scrape",
            12: "learn",
            13: "trade"
        }

        # negative 1 is defined as exit

        selections = {
            "main": [1, 2, -1],
            "display": [3, 4, 5, 6, 7, 8, 9, 10, 0],
            "actions": [11, 12, 13, 0],
            "stocks": [-2, -3, -4, 1],
            "bonds": [-2, -3, -4, 1],
            "currency": [-2, -3, -4, 1],
            "etf": [-2, -3, -4, 1],
            "future": [-2, -3, -4, 1],
            "index": [-2, -3, -4, 1],
            "mutual": [-2, -3, -4, 1],
            "warrant": [-2, -3, -4, 1],
            "scrape": [-2,-3,2],
            "learn": [-2,2],
            "trade": [-2,2]
        }

        return selections[pages[current_page]][input - 1]

    def display(self, page):

        file = open(self.files[page], "r+")
        total_file = file.read()

        data = json.loads(total_file)

        search_index = 0

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("THE ELEMENT")
            print("element: " + str(search_index + 1) + " out of " + str(len(data)) + "\n")
            if data[search_index]["Ticker"]:
                print("     Ticker: " + str(data[search_index]["Ticker"]))

            if data[search_index]["Name"]:
                print("     Name: " + str(data[search_index]["Name"]))

            if data[search_index]["Exchange"]:
                print("     Exchange: " + str(data[search_index]["Exchange"]))

            if page == 3:
                if data[search_index]["categoryName"]:
                    print("     Catagory: " + str(data[search_index]["categoryName"]))

                if data[search_index]["categoryNr"]:
                    print("     Number: " + str(data[search_index]["categoryNr"]))

            print("\n\n[1] previous\n[2] next\n[3] add to prospective\n[4] exit\n\n")

            selection = input('Please Choose a selection: ')
            selection =  int(selection)

            if selection == 4:
                break

            if selection == 1:
                search_index = search_index - 1

            if selection == 2:
                search_index = search_index + 1

            if search_index < 0:
                search_index = 0

            if search_index > (len(data) - 1):
                search_index = len(data) - 1

            if selection == 3:
                returned_object = self.function_definitions[page](data[search_index]["Ticker"], data[search_index]["Name"],
                                           data[search_index]["Exchange"], data[search_index]["categoryName"],
                                           data[search_index]["categoryNr"])

                self.current_prospects.append(returned_object)
                print(self.current_prospects)
                toss_it = input('Press anything to continue: ')

        # array dictionary ticker stock objects
        return data

    def search(self, page):
        search_array = []
        name_dict = {
            0: "Ticker",
            1: "Name",
            2: "Exchange",
            3: "categoryName",
            4: "categoryNr"
        }
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Select element to search by:\n\n")

            print("[1] Ticker")
            print("[2] Name")
            print("[3] Exchange")
            if page == 3:
                print("[4] Category")
                print("[5] Number")

            print("\n\n")

            selection = input('Please Choose a selection: ')
            selection =  int(selection)

            os.system('cls' if os.name == 'nt' else 'clear')
            print(name_dict[selection-1]+"\n\n")
            termOutput = input('Please Type a search Term: ')

            file = open(self.files[page], "r+")
            total_file = file.read()

            data = json.loads(total_file)

            for element in data:
                if str(termOutput) in str(element[name_dict[selection-1]]):
                    returned_object = self.function_definitions[page](element["Ticker"],
                                                                      element["Name"],
                                                                      element["Exchange"],
                                                                      element["categoryName"],
                                                                      element["categoryNr"])
                    search_array.append(returned_object)

            break

        print(search_array)
        print("\n\n\n")

        toss_it = input('[y] to add to prospective list, anything else to continue: ')

        if "y" in toss_it:
            self.current_prospects = self.current_prospects + search_array

        return

    def append(self, page):
        file = open(self.files[page], "r+")
        total_file = file.read()
        data = json.loads(total_file)
        for search_index in data:
            returned_object = self.function_definitions[page](search_index["Ticker"], search_index["Name"],
                                                         search_index["Exchange"], search_index["categoryName"],
                                                         search_index["categoryNr"])

            self.current_prospects.append(returned_object)

        print(self.current_prospects)

        return

    def email_crawler(self, new_url, web_name):
        epoch_timestamp = int(calendar.timegm(time.gmtime()))
        epoch_timestamp += 420
        new_urls = deque(new_url)
        processed_urls = set()
        emails = set()

        while len(new_urls):
            url = new_urls.popleft()
            processed_urls.add(url)

            parts = urlsplit(url)
            base_url = "{0.scheme}://{0.netloc}".format(parts)
            path = url[:url.rfind('/') + 1] if '/' in parts.path else url

            print("Processing %s" % url)
            try:
                response = requests.get(url)
            except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

            remove_set = set()

            for set_email in new_emails:
                if ".png" in set_email:
                    remove_set.add(set_email)
                if ".jpg" in set_email:
                    remove_set.add(set_email)
                if ".jpeg" in set_email:
                    remove_set.add(set_email)
                if "email.com" in set_email:
                    remove_set.add(set_email)

            for email in remove_set:
                new_emails.remove(email)

            epoch_timestamp_new = int(calendar.timegm(time.gmtime()))

            if epoch_timestamp_new > epoch_timestamp:
                break

            emails.update(new_emails)
            print(emails)

            soup = BeautifulSoup(response.text)

            for anchor in soup.find_all("a"):
                link = anchor.attrs["href"] if "href" in anchor.attrs else ''
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link
                if not link in new_urls and not link in processed_urls:
                    new_urls.append(link)

        for element in list(emails):
            database_emails = dict()

            database_emails['names'] = web_name
            database_emails['url'] = url
            database_emails['email'] = element

            result = self.db.EmailScraper.insert_one(database_emails)
            print(result.inserted_id)

    def scrape_google(self):
        for element in self.current_prospects:
            # search for urls
            instance = bot.Bot("abhishekpratapa@utexas.edu", "BedruSe7", "5129831767", bot.Sites.Google,
                                   bot.UserAgent.Firefox, True, "mongodb://localhost:27017", ["Google_Data_Base"])
            returned_URLs = instance.search([element["name"]], 10, [], "0/0/0", "0/0/0", 0, "companies")
            instance.close()
            #search for emails
            for urls in returned_URLs:
                t = Thread(target=self.email_crawler, args=(urls, element["name"],))
                t.start()

        return

    def scrape_linkedin(self):
        for element in self.current_prospects:
            instance = bot.Bot("abhishekpratapa@gmail.com", "AlinaSchroeder#123", "5129831767", bot.Sites.LinkedIn,
                               bot.UserAgent.Firefox, True, "mongodb://localhost:27017", ["LinkedIn_Data_Base"])
            instance.siteAgent.search(element["name"], 20, True, True, 3)
            instance.close()
        return

    def learn_articles(self):
        start_date = date(2009, 1, 2)
        end_date = date(2016, 6, 2)
        previous_data = "01/01/2009"

        instance = bot.Bot("abhishekpratapa@utexas.edu", "BedruSe7", "5129831767", bot.Sites.Google,
                           bot.UserAgent.Firefox, True, "mongodb://localhost:27017", ["Article_Data_Base"])
        recurrent = 1
        nextOne = 0
        for single_date in daterange(start_date, end_date):
            if nextOne % 2 == 0:
                previous_data = str(single_date.strftime("%m/%d/%Y"))
                print(nextOne)
                nextOne += 1
                continue
            nextOne += 1
            for element in self.current_prospects:
                # search for urls
                returned_URLs = instance.search([element["name"]], 10, [], previous_data, str(single_date.strftime("%m/%d/%Y")), 0, "article", "cnn.com", recurrent)

                recurrent += 1

                for url in returned_URLs:
                    incept = dict()
                    incept['name'] = element["name"]
                    incept['ticker'] = element["ticker"]
                    incept['url'] = url
                    incept['start_date'] = str(start_date.strftime("%m/%d/%Y"))
                    incept['end_date'] = str(end_date.strftime("%m/%d/%Y"))
                    self.db.stock_urls.insert_one(incept)

                returned_urls_2 = instance.search([element["ticker"]], 10, [], previous_data, str(single_date.strftime("%m/%d/%Y")), 0, "article", "cnn.com",recurrent)
                previous_data = str(single_date.strftime("%m/%d/%Y"))

                for url in returned_urls_2:
                    incept = dict()
                    incept['name'] = element["name"]
                    incept['ticker'] = element["ticker"]
                    incept['url'] = url
                    incept['start_date'] = str(start_date.strftime("%m/%d/%Y"))
                    incept['end_date'] = str(end_date.strftime("%m/%d/%Y"))
                    self.db.stock_urls.insert_one(incept)

        instance.close()
        return
    def trade_stocks(self):
        pass
    def display_apporiate_data(self, choice, page):

        if (page >= 3 and page <= 10):
            # dictionary of functions
            options = {
                2: self.display,
                3: self.search,
                4: self.append
            }

            # options function
            options[choice](page)
            return choice
        elif (page == 11):
            options = {
                2: self.scrape_google,
                3: self.scrape_linkedin
            }

            t = Thread(target=options[choice], args=())
            t.start()

            return choice
        elif (page == 12):
            options = {
                2: self.learn_articles
            }

            t = Thread(target=options[choice], args=())
            t.start()

            return choice
        elif (page == 13):
            options = {
                2: self.trade_stocks
            }

            t = Thread(target=options[choice], args=())
            t.start()

            return choice
        # return form function
        return choice

new_stock_agent = Stocks()