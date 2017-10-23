import csv
import urllib.request
import json
import pandas as pd
import numpy as np
from sklearn.externals import joblib

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

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for parti in range(0, len(l), n):
        yield l[parti:parti + n]

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
authors = {}
authordictionary = {}
authortopicdict = {}

with open("papers/authortopic.csv") as authortopic:
    authortopicreader = csv.DictReader(authortopic, delimiter=",", quotechar="\"")
    for row in authortopicreader:
        topicsforauthor = ast.literal_eval(row["topics"])

        nicelist = []

        for topicsrow in topicsforauthor:
            topic = topics[str(topicsrow[0])]
            nicelist.append({"topicid": topicsrow[0], "amount": topicsrow[1], "topicname": topic["name"]})

        authortopicdict[row["id"]] = nicelist

with open("papers/new_authors.csv") as authorsfile:
    authorreader = csv.DictReader(authorsfile, delimiter=",", quotechar="\"")
    for row in authorreader:
        author = {"id": row["id"], "name": row["name"],
                  "rank": int(authorranks[authorranks["id"] == int(row["id"])]["PageRankRank"].values[0]),
                  "score": float(authorranks[authorranks["id"] == int(row["id"])]["PageRankScore"].values[0]),
                  "articles": row["numArticles"], "minyear": row["minYear"], "maxyear": row["maxYear"],
                  "topics":authortopicdict[row["id"]], "relauthors": []}
        authors[int(row['id'])] = author
        authordictionary[row["id"]] = author

cluster_author = joblib.load('papers/cluster_author_dictionary') # key is author id,
for key, values in cluster_author.items():
    for aut in values:
        aid = int(aut['author id'])
        author = authors[aid]
        aut['name'] = author['name']
        aut['pagerank'] = int(aut['pagerank'])
    for aut1 in values:
        author = authors[aut1['author id']]
        for aut2 in values:
            if aut1['author id'] != aut2['author id']:
                author['relauthors'].append(aut2)
        sorted_list = sorted(author['relauthors'], key=lambda k: k['pagerank'], reverse=True)
        author['relauthors'] = sorted_list

data = list(authors.values())
put_request("http://localhost:5002/authors", json.dumps(data).encode())

print("Imported authors")

a = pd.read_csv("papers/new_paper_authors.csv")
b = pd.read_csv("papers/new_authors.csv")
b.columns = ['author_id', 'name', "articles", "minyear", "maxyear"]
b = b.dropna(axis=1)
merged = a.merge(b, on='author_id')

genabstracts = pd.read_csv("papers/gen_abstracts.csv")
genabstracts.columns = ['paper_id', 'gen_abstract']

for row in merged.itertuples():
    author = authordictionary[str(row.author_id)]
    author['relauthors'] = None
    dict[str(row.paper_id)]['authors'].append(author)

for gen_abstract in genabstracts.itertuples():
    if type(gen_abstract.gen_abstract) is float:
        dict[str(gen_abstract.paper_id)]['gen_abstract'] = ""
    else:
        dict[str(gen_abstract.paper_id)]['gen_abstract'] = gen_abstract.gen_abstract

papers = {}
ids = []
processed_papers = []
for key, value in dict.items():
    value["references"] = []
    value["referencedby"] = []
    value["relpapers"] = []
    papers[value['id']] = value
    ids.append(int(value['id']))

print("Processed papers")

a = pd.read_csv("papers/id_cluster_hierarchical40.csv")
grouped = a.groupby(['cluster'])

#Generate all possible combinations with regards to clusters
combinations = []
j = 0

done_clusters = 0

for name, group in grouped:
    if done_clusters == 100:
        print("Cluster {0}".format(name))
        done_clusters = 0
    paper_ids = (list(group['id']))
    for id1 in paper_ids:
        for id2 in paper_ids:
            if id1 != id2:
                entry = [id1, id2]
                combinations.append(entry)

    done_clusters = done_clusters + 1

#For each combination save cosine sim, title and author
d = np.load('papers/cosine_similarity.npy')
i = 0
for tuple in combinations:
    if i % 10000 == 0:
        print("{0} of {1}".format(i, len(combinations)))
    paper_one = papers[str(tuple[0])]
    paper_two = papers[str(tuple[1])]
    cosim = d[ids.index(tuple[0])][ids.index(tuple[1])].item()
    entry = {}
    entry['id'] = int(tuple[1])
    entry['sim'] = cosim
    entry['title'] = paper_two['title']
    entry['authors'] = paper_two['authors']
    entry['year'] = paper_two['year']
    paper_one['relpapers'].append(entry)
    i+=1

paperpageranks = {}

with open("papers/PaperPageRank.csv") as paperpagerankfile:
    paperpagerankreader = csv.DictReader(paperpagerankfile)

    for row in paperpagerankreader:
        paperpageranks[row["paper_id"]] = row


#sort on cosime sim
for key, value in papers.items():
    sorted_list = sorted(value['relpapers'], key=lambda k: k['sim'], reverse=True)
    value['relpapers'] = sorted_list
    value["references"] = []
    value["referencedby"] = []

    topics = papertopic[value["id"]]

    value["year"] = int(value["year"])

    if topics:
        value["topics"] = topics
    else:
        value["topics"] = []

    value["rank"] = paperpageranks[value["id"]]["pagerankrank"]
    value["score"] = float(paperpageranks[value["id"]]["pagerank"])



    # for topic in value["topics"]:
    #   topic["rank"] = paperpageranks[value["id"]]["T" + topic["id"] + "PRRank"]
    #   topic["score"] = float(paperpageranks[value["id"]]["T" + topic["id"] + "PRScore"])

papers_to_send = list(papers.items())

papers = {}

for subset in chunks(papers_to_send, 1000):
    put_request("http://localhost:5002/papers", json.dumps(list([x[1] for x in subset])).encode())



print("Imported papers")

refs = []

with open("papers/citation_graph.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
    for row in reader:
        refs.append({"Source": row["Source"], "Target": row["Target"]})

put_request("http://localhost:5002/references", json.dumps(refs).encode())
