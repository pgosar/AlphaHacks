import requests
import re
from bs4 import BeautifulSoup
import json
import uuid
import time


def json_sources():
    with open("sources.json", "r") as f:
        return json.load(f)


def rss(srcs="default"):
    SOURCES = json_sources()
    article_list = []
    if srcs == "all":
        sources = SOURCES.keys()
    else:
        sources = srcs.split(",")
    for source in sources:
        for url in SOURCES[source]:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.content, features="xml")
                articles = soup.findAll("item")
                for a in articles:
                    title = a.find("title").text
                    link = a.find("link").text
                    description = a.find("description").text
                    description = re.sub(r"[^A-Za-z0-9 ]+", "", description)
                    published = a.find("pubDate").text
                    uid = str(uuid.uuid4())
                    article = {"id": uid,
                               "source": source,
                               "data": {
                                   "title": title,
                                   "link": link,
                                   "description": description,
                                   "published": published
                               }}
                    article_list.append(article)
            except Exception as e:
                print("The scraping job failed. See exception:")
                print(e)

    with open("metadata.json", "w") as outfile:
        json.dump(article_list, outfile)

    return article_list


def scrape(string):
    print("Downloading metadata...")
    al = rss(string)
    for i in range(10):
        print(al[i]["data"]["description"])
    print(f"Articles Scraped: {len(al)}")
    print("Initializing metric classifier...")


if __name__ == "__main__":
    scrape("all")
