# -*- coding: utf-8 -*-
#%%
import glob
import json
import pandas as pd
import sys

from contextlib import suppress
from newsapi import NewsApiClient
from newspaper import Article

from utilities import print_dataframe

#%%
newsapi_key = '38b178162f2e497cb564c6a6dafc6c9a'

#%%
def process_article(url):
    article_text = ""
    with suppress(Exception):
        article = Article(url)
        article.download()
        article.parse()
        article_text = article.text
    # print(article_text)
    return article_text

#%%
def process_urls(json_data):
    processed = []
    print("Processing " + str(len(json_data["articles"])))
    for article in json_data["articles"]:
        with suppress(Exception):
            print("Scrapping " + article["url"])
            article["fullarticle"] = process_article(article["url"])
            processed.append(article)
    # source, author, content, description, fullarticle, publishedAt, title, url, urlToImage
    data = pd.DataFrame.from_dict(processed)
    # print_dataframe(data)
    return data

#%%
def trigger_local(json_path):
    local_df = []
    for file in glob.glob(json_path + "\\*.json"):
        print("Processing " + file)
        with open(file, encoding="utf8") as jsonFile:
            with suppress(Exception):
                local_df = process_urls(json.load(jsonFile))
    return local_df

#%%
def trigger_remote(search_query, article_count=1, sort="relevancy"):
    remote_df = []
    print("searching for " + search_query)
    api = NewsApiClient(api_key=newsapi_key)
    with suppress(Exception):
        news_json = api.get_everything(
            q=search_query,
            page_size=int(article_count), sort_by=sort)
        # print(news_json)
        with suppress(Exception):
            remote_df = process_urls(news_json)
    return remote_df

#%%
# print(trigger_local("D:\\Workspace\\github\\be_my_voice\\.dump"))
# print(trigger_remote("poaching and rhino", 10))
