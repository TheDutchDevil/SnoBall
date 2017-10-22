import csv
import urllib.request
import json
import requests


class RequestWithMethod(urllib.request.Request):
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        urllib.request.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        return self._method if self._method else super(RequestWithMethod, self).get_method()


def put_request(url, data):
    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    request = RequestWithMethod(url, method='PUT', data=data, headers={'Content-Type': 'application/json'})
    return opener.open(request)


def get_request(url):
    opener = urllib.request.build_opener(urllib.request.HTTPHandler)
    request = RequestWithMethod(url, method='GET', headers={'Content-Type': 'application/json', 'Connection': 'close'})
    return opener.open(request)


topics = get_request("http://localhost:5002/topics")
topic_results = json.loads(topics.read())['result']

topics = []

for topic_raw in topic_results:
    topic = {}
    topic["id"] = topic_raw["id"]
    topic["name"] = topic_raw["name"]
    topic["keywords"] = topic_raw["keywords"]

    topics.append(topic)

put_request("http://localhost:2222/topics", json.dumps(topics).encode())

authors = get_request("http://localhost:5002/authors")
author_results = json.loads(authors.read())['result']

authors = []

for author_raw in author_results:
    author = {}
    author["id"] = author_raw["id"]
    author["name"] = author_raw["name"]
    author["rank"] = author_raw["rank"]
    author["score"] = author_raw["score"]
    authors.append(author)

put_request("http://localhost:2222/authors/many", json.dumps(authors).encode())

papers = get_request("http://localhost:5002/papers")
results = json.loads(papers.read())['result']

papers = []

for temp in results:
    paper = {}
    paper["id"] = temp["id"]
    paper["title"] = temp["title"]
    paper["authors"] = temp["authors"]
    if temp["gen_abstract"]:
        paper["gen_abstract"] = temp["gen_abstract"]
    else:
        paper["gen_abstract"] = ""
    if temp["abstract"] != "Abstract Missing":
        paper["paperAbstract"] = temp["abstract"]
    paper["paperBody"] = temp["paper_text"]
    paper["rank"] = temp["rank"]
    paper["score"] = temp["score"]
    paper["year"] = temp["year"]
    header = {"Content-Type": "application/json"}
    papers.append(paper)

put_request("http://localhost:2222/papers/many", json.dumps(papers).encode())
