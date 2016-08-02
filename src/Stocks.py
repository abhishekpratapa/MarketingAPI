import os


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
    return mutual_fund_element


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
    return warrant_element


def display_options(index=0):

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
        "SCRAPE",
        "LEARN",
        "TRADE"
    ]

    print(options[index])


def return_relevant_page(current_page, input):
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
        "main": [1,2,-1],
        "display": [3, 4, 5, 6, 7, 8, 9, 10, 0],
        "actions": [11, 12, 13, 0],
        "stocks": [0,0,0,1],
        "bonds": [0,0,0,1],
        "currency": [0,0,0,1],
        "etf": [0,0,0,1],
        "future": [0,0,0,1],
        "index": [0,0,0,1],
        "mutual": [0,0,0,1],
        "warrant": [0,0,0,1],
        "scrape": [],
        "learn": [],
        "trade": []
    }

    return selections[pages[current_page]][input-1]


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

        # fill this with potential array hits
        self.current_prospects = []

        # check if the user wants terminal access
        if terminal:
            self.terminal()

    # This part of the program takes care of the user inputs
    def terminal(self):
        # Loop the program
        while True:

            # Clear the screen and display the relevant information
            os.system('cls' if os.name == 'nt' else 'clear')
            display_options(self.current_window)

            # Select what to do next
            selection = input('Please Choose a selection: ')
            self.current_window = return_relevant_page(self.current_window, int(selection))

            # Exit program
            if self.current_window == -1:
                exit()

    def scrape_articles(self, website):

        pass

new_stock_agent = Stocks()