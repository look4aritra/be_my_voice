import json
import glob
import pandas as pd

from newspaper import Article


def processarticle(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        print(article.text)
        return article.text
    except:
        return ""


for file in glob.glob("C:\\Users\\Pratim\\Desktop\\dump\\*.json"):
    processed = []
    print("Processing " + file)
    with open(file, encoding="utf8") as jsonFile:
        try:
            data = json.load(jsonFile)
            for article in data["articles"]:
                print(article["url"])
                article["fullarticle"] = processarticle(article["url"])
                processed.append(article)
        except:
            print("unable to process "+file)
    # source, author, content, description, fullarticle, publishedAt, title, url, urlToImage
    df = pd.DataFrame.from_dict(processed)
    print(df)
