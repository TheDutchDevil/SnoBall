import csv
import urllib.request
import json
import pandas as pd
import numpy as np
import math


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
        author = {"id": row["id"], "name": row["name"], "rank": int(authorranks[authorranks["id"] == int(row["id"])]["PageRankRank"].values[0])}
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
    dict[str(row.paper_id)]['authors'].append({"name":row.name, "id":row.author_id.item()})

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
for name, group in grouped:
    print("Cluster {0}".format(name))
    paper_ids = (list(group['id']))
    for id1 in paper_ids:
        for id2 in paper_ids:
            if id1 != id2:
                entry = [id1, id2]
                combinations.append(entry)

#For each combination save cosine sim, title and author
d = np.load('papers/cosine_similarity.npy')
i = 0
for tuple in combinations:
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

#sort on cosime sim
for key, value in papers.items():
    sorted_list = sorted(value['relpapers'], key=lambda k: k['sim'], reverse=True)
    value['relpapers'] = sorted_list

data = json.dumps(list(papers.values()))
put_request("http://localhost:5002/papers", data.encode())

print("Imported papers")

refs = []

with open("papers/citation_graph.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar="\"")
    for row in reader:
        refs.append({"Source": row["Source"], "Target": row["Target"]})

put_request("http://localhost:5002/references", json.dumps(refs).encode())

