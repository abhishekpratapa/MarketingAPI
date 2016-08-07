from pymongo import MongoClient
from newspaper import Article
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import time
import finsymbols

client = MongoClient("mongodb://localhost:27017")
db = client.cnn_scrape

elements = db.raw_articles.find()
sid = SentimentIntensityAnalyzer()
sp500 = finsymbols.get_sp500_symbols()

for ele in sp500:
    for ele in elements:
        initiation = dict()
        print(ele["url"])
        initiation["url"] = ele["url"]
        print(ele["ticker"])
        initiation["ticker"] = ele["ticker"]
        print(ele["summary"])
        initiation["summary"] = ele["summary"]
        print(ele["date"])
        initiation["date"] = ele["date"]
        article = Article(ele["url"])
        article.download()
        time.sleep(5)
        if article.html == '':
            continue
        initiation["html"] = article.html
        article.parse()
        article.nlp()
        list_empty = []
        lines_list = tokenize.sent_tokenize(article.text)
        for sentence in lines_list:
            tokens_empty = dict()
            ss = sid.polarity_scores(sentence)
            for k in sorted(ss):
                tokens_empty[str(k)] = str(ss[k])
                textit = str(k) + " " + str(ss[k])
                print(textit)
            list_empty.append(tokens_empty)
        initiation["scores"] = list_empty
        print(str(article.summary))
        initiation["nlp_summary"] = article.summary
        print(str(article.keywords))
        initiation["nlp_keywords"] = article.keywords
        print(str(article.publish_date))
        initiation["nlp_publish_date"] = article.publish_date
        db.learning.insert_one(initiation)
        time.sleep(6)