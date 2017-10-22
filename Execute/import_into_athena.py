import csv
import urllib.request
import json
import pandas as pd
import math
import ast


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


topics = {}

with open("papers/topics.csv") as topicsfile:
    topicreader = csv.DictReader(topicsfile, delimiter=",", quotechar="\"")
    for row in topicreader:
        topic = {}

        topic["id"] = row["id"]

        topic["name"] = row["topicname"]

        topic["keywords"] = []

        for topic_tuple in ast.literal_eval(row["keywords"]):
            topic["keywords"].append(topic_tuple)

        topic["occurence"] = row["occurence"]

        topic["occurence_yearly"] = ast.literal_eval(row["occurence_yearly"])

        topics[row["id"]] = topic

put_request('http://localhost:5002/topics', json.dumps(list(topics.values())).encode())

papertopic = {}

with open("papers/paperid_topic.csv") as topicpaperfile:
    topicpaperreader = csv.DictReader(topicpaperfile, delimiter=",", quotechar="\"")

    for row in topicpaperreader:
        topicsofpaper = []

        for topicsofpaperraw in ast.literal_eval(row["topics"]):
            topicsofpaper.append(topics[str(topicsofpaperraw[0])])

        papertopic[row["id"]] = topicsofpaper

print("Imported topics")

dict = {}

with open("papers/papers.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
    for row in reader:
        row["authors"] = []
        dict[row['id']] = row

authorranks = pd.read_csv("papers/AuthorPageRank.csv")

authors = []

with open("papers/new_authors.csv") as authorsfile:
    authorreader = csv.DictReader(authorsfile, delimiter=",", quotechar="\"")
    for row in authorreader:
        author = {"id": row["id"], "name": row["name"],
                  "rank": int(authorranks[authorranks["id"] == int(row["id"])]["PageRankRank"].values[0]),
                  "score": float(authorranks[authorranks["id"] == int(row["id"])]["PageRankScore"].values[0])}
        authors.append(author)

put_request("http://localhost:5002/authors", json.dumps(authors).encode())

print("Imported authors")

a = pd.read_csv("papers/new_paper_authors.csv")
b = pd.read_csv("papers/new_authors.csv")
b.columns = ['author_id', 'name']
b = b.dropna(axis=1)
merged = a.merge(b, on='author_id')

genabstracts = pd.read_csv("papers/gen_abstracts.csv")
genabstracts.columns = ['paper_id', 'gen_abstract']

for row in merged.itertuples():
    dict[str(row.paper_id)]['authors'].append({"name": row.name, "id": row.author_id.item()})

for gen_abstract in genabstracts.itertuples():
    if type(gen_abstract.gen_abstract) is float:
        dict[str(gen_abstract.paper_id)]['gen_abstract'] = ""
    else:
        dict[str(gen_abstract.paper_id)]['gen_abstract'] = gen_abstract.gen_abstract

paperpageranks = {}

with open("papers/PaperPageRank.csv") as paperpagerankfile:
    paperpagerankreader = csv.DictReader(paperpagerankfile)

    for row in paperpagerankreader:
        paperpageranks[row["paper_id"]] = row

papers = []

for key, value in dict.items():

    value["references"] = []
    value["referencedby"] = []

    topics = papertopic[value["id"]]

    value["year"] = int(value["year"])

    if topics:
        value["topics"] = topics
    else:
        value["topics"] = []

    value["rank"] = 3 #paperpageranks[value["id"]]["pagerankrank"]
    value["score"] = 0.4 # float(paperpageranks[value["id"]]["pagerank"])

    # for topic in value["topics"]:
    #   topic["rank"] = paperpageranks[value["id"]]["T" + topic["id"] + "PRRank"]
    #   topic["score"] = float(paperpageranks[value["id"]]["T" + topic["id"] + "PRScore"])

    papers.append(value)

print("Processed papers")

data = json.dumps(papers)
put_request("http://localhost:5002/papers", data.encode())

print("Imported papers")

refs = []

with open("papers/citation_graph.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
    for row in reader:
        refs.append({"Source": row["Source"], "Target": row["Target"]})

put_request("http://localhost:5002/references", json.dumps(refs).encode())
