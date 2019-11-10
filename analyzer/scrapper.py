import json
import glob
import pandas as pd
import sys

from newsapi import NewsApiClient
from newspaper import Article

apikey = '38b178162f2e497cb564c6a6dafc6c9a'
query = "poaching and rhino"


def processarticle(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        # print(article.text)
        return article.text
    except:
        return ""


def processurls(jsonData):
    processed = []
    print("Processing " + str(len(jsonData["articles"])))
    for article in jsonData["articles"]:
        try:
            print("Scrapping " + article["url"])
            article["fullarticle"] = processarticle(article["url"])
            processed.append(article)
        except:
            print("unable to process " + article["url"])
    # source, author, content, description, fullarticle, publishedAt, title, url, urlToImage
    data = pd.DataFrame.from_dict(processed)
    return data


df = []
if sys.argv[1] == "local":
    for file in glob.glob("C:\\Users\\Pratim\\Desktop\\dump\\*.json"):
        print("Processing " + file)
        with open(file, encoding="utf8") as jsonFile:
            try:
                data = json.load(jsonFile)
                df = processurls(data)
            except:
                print("unable to process "+file)

else:
    print("searching for " + sys.argv[3])
    api = NewsApiClient(api_key=apikey)
    newsjson = api.get_everything(
        q=sys.argv[3],
        page_size=int(sys.argv[2]), sort_by='relevancy')
    # print(newsjson)
    try:
        df = processurls(newsjson)
    except:
        print("unable to process query")

for row in df.itertuples(index=False):
    print(row)
