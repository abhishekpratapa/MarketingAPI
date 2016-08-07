import requests
import json
import pprint
#cookies = dict()
#cookies["crtg_trnr"] = ""
#cookies["RT"] =
import re
import time
import finsymbols
from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.cnn_scrape

def get_get_response(searchTerm):
    searchTerm = re.sub('[^A-Za-z0-9 ]+', '', searchTerm)
    searchTerm = searchTerm.replace(" ", "+")
    print(searchTerm)

    # parts one
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    #first request
    response = requests.get("http://searchapp.cnn.com/money-search/query.jsp?query="+str(searchTerm)+"&type=article&start="+str("1")+"&npp=10&s=all&primaryType=article&sortBy=date&csiID=csi4", headers=headers)

    print(response.status_code)

    response_string = response.text.split('<textarea id="jsCode">')[1].split("</textarea>")[0].split("     {")[1]
    response_string = "{"+response_string
    response_string = response_string.split("}\n")[0]
    response_string = response_string + "}"

    print(response_string)

    object_returnable = json.loads(response_string)

    starts_at = object_returnable["criteria"][0]["startAt"]
    max_results = object_returnable["criteria"][0]["maxResults"]
    num_queries_1 = object_returnable["metaResults"]["article"]

    if num_queries_1 == 0:
        return False

    index = 1

    while num_queries_1 > index:

        # parts one
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        }

        # first request
        response = requests.get(
            "http://searchapp.cnn.com/money-search/query.jsp?query=" + str(searchTerm) + "&type=article&start=" + str(index) + "&npp=10&s=all&primaryType=article&sortBy=date&csiID=csi4", headers=headers)

        response_string = response.text.split('<textarea id="jsCode">')[1].split("</textarea>")[0].split("     {")[1]
        response_string = "{" + response_string
        response_string = response_string.split("}\n")[0]
        response_string = response_string + "}"

        object_returnable = json.loads(response_string)

        max_results = object_returnable["criteria"][0]["maxResults"]

        for obj in object_returnable["results"][0]:
            init = dict()
            init["search"] = searchTerm
            init["more_data"] = obj

            db.raw_articles.insert_one(init)

            print(init)

        index = 1 + max_results

        time.sleep(1)

    return True

def calculateParallel(numbers, threads=2):
    pool = ThreadPool(threads)
    results = pool.map(get_get_response, numbers)
    pool.close()
    pool.join()
    return results

sp500 = finsymbols.get_sp500_symbols()
empty_array = []

for ticker in sp500:
    empty_array.append(ticker["company"])

calculateParallel(empty_array, 16)