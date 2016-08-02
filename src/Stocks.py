

def stocks_dictionary(ticker, name, exchange, catagory, catagory_number):
    stock_element = dict()
    stock_element['ticker'] = ticker
    stock_element['name'] = name
    stock_element['exchange'] = exchange
    stock_element['catagory'] = catagory
    stock_element['catagory_number'] = catagory_number
    return stock_element


def currency_dictionary(ticker, name, exchange):
    currency_element = dict()
    currency_element['ticker'] = ticker
    currency_element['name'] = name
    currency_element['exchange'] = exchange
    return currency_element


def etf_dictionary(ticker, name, exchange):
    etf_element = dict()
    etf_element['ticker'] = ticker
    etf_element['name'] = name
    etf_element['exchange'] = exchange
    return etf_element


def future_dictionary(ticker, name, exchange):
    future_element = dict()
    future_element['ticker'] = ticker
    future_element['name'] = name
    future_element['exchange'] = exchange
    return future_element


def index_dictionary(ticker, name, exchange):
    index_element = dict()
    index_element['ticker'] = ticker
    index_element['name'] = name
    index_element['exchange'] = exchange
    return index_element


def mutual_fund_dictionary(ticker, name, exchange):
    mutual_fund_element = dict()
    mutual_fund_element['ticker'] = ticker
    mutual_fund_element['name'] = name
    mutual_fund_element['exchange'] = exchange
    return mutual_fund_element


def warrant_dictionary(ticker, name, exchange):
    warrant_element = dict()
    warrant_element['ticker'] = ticker
    warrant_element['name'] = name
    warrant_element['exchange'] = exchange
    return warrant_element


class Stocks:
    def __init__(self, gui_index=True):
        if gui_index:
            self.gui_field()
        pass

    def gui_field(self):
        

        pass

    def scrape(self):
        pass
