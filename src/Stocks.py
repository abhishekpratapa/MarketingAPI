
def stocks_dictionary(ticker, name, exchange, catagory, catagory_number):
    stock_element = dict()
    stock_element['ticker'] = ticker
    stock_element['name'] = name
    stock_element['exchange'] = exchange
    stock_element['catagory'] = catagory
    stock_element['catagory_number'] = catagory_number
    return stock_element

class Stocks:
    def __init__(self, gui_index=True):
        if gui_index:
            self.gui_field()
        pass

    def gui_field(self):
        pass

    def scrape(self):
        pass
