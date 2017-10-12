import csv
import urllib.request
import json
import pandas as pd


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

authors = []

with open("papers/new_authors.csv") as authorsfile:
    authorreader = csv.DictReader(authorsfile, delimiter=",", quotechar="\"")
    for row in authorreader:
        author = {"id": row["id"], "name": row["name"]}
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
    dict[str(row.paper_id)]['authors'].append(row.name)

for gen_abstract in genabstracts.itertuples():
    dict[str(gen_abstract.paper_id)]['gen_abstract'] = gen_abstract.gen_abstract

papers = []

for key, value in dict.items():
    papers.append(value)

print("Processed papers")

data = json.dumps(papers)
put_request("http://localhost:5002/papers", data.encode())

print("Imported papers")


