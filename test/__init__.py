from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from pymongo import MongoClient
import time
import re
import finsymbols
from multiprocessing.dummy import Pool as ThreadPool
from pyvirtualdisplay import Display

def get_store_articles_in_database(searchEvent):
    searchEvent = str(searchEvent)
    print(searchEvent)
    client = MongoClient("mongodb://localhost:27017")
    db = client.cnn_scrape

    #display = Display(visible=False, size=(1980, 1024))
    #display.start()

    driver = webdriver.Chrome()
    driver.get("http://money.cnn.com/")

    time.sleep(10)

    searchBar = driver.find_element_by_id("symb")
    searchBar.send_keys(searchEvent)
    searchBar.send_keys(Keys.ENTER)

    time.sleep(3)

    try:
        link_to_click = driver.find_element_by_id("moneyTotalArticles")
        article_Numbers= link_to_click.find_element_by_tag_name("em")
        total_value = article_Numbers.get_attribute("innerHTML")

        integer_limit = int(total_value.replace('(', '').replace(')', ''))
        print(integer_limit)
        link_to_click.click()
    except:
        driver.close()
        #display.stop()
        return "False"
    index = 0
    previous_integer=-1
    time.sleep(3)

    while index < integer_limit:

        if index == previous_integer:
            break
        else:
            previous_integer = index

        time.sleep(10)
        
        article_container = driver.find_element_by_id("summaryList_articles")
        number_of_elements = article_container.find_elements_by_class_name("summaryBlock")

        for ele in number_of_elements:
            index += 1
            try:
                headline = ele.find_element_by_class_name("cnnHeadline")
                tagged = headline.find_element_by_tag_name("a")
                link = tagged.get_attribute("href")
                print(link)

                attribute_searched = ele.find_element_by_class_name("cnnBlurbTxt")
                text_summary = attribute_searched.get_attribute("innerHTML")
                text_summary = re.sub('<[^<]+?>', '', text_summary)
                print(text_summary)

                the_date = ele.find_element_by_class_name("cnnDateStamp")
                date_returned = the_date.get_attribute("innerHTML")
                print(date_returned)

                init_data = dict()
                init_data["url"] = link
                init_data["company"] = searchEvent
                init_data["summary"] = text_summary
                init_data["date"] = date_returned

                db.raw_articles.insert_one(init_data)
            except:
                pass

        next_button = driver.find_elements_by_class_name("next")

        next_button_pressed = False

        for element in next_button:
            if "ends next" in element.get_attribute("class"):
                try:
                    element.click()
                    next_button_pressed = True
                    break
                except:
                    pass

        print(next_button_pressed)

        time.sleep(5)
    driver.close()
    #display.stop()
    return "True"

sp500 = finsymbols.get_sp500_symbols()

tickerArray = []

for ticker in sp500:
    value = ticker["company"]
    print("________________________________________________")
    print("________________________________________________")
    print("________________________________________________")
    print("________________________________________________")
    get_store_articles_in_database(value)
    print("________________________________________________")
    print("________________________________________________")
    print("________________________________________________")
    print("________________________________________________")
# get_store_articles_in_database("GOOGL")
