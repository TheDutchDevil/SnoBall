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
    reader = csv.DictReader(csvfile, delimiter =",", quotechar="\"")
    for row in reader:
        row["authors"] = []
        dict[row['id']] = row

a = pd.read_csv("papers/new_paper_authors.csv")
b = pd.read_csv("papers/authors.csv")
b.columns = ['author_id', 'name']
b = b.dropna(axis=1)
merged = a.merge(b, on='author_id')

for row in merged.itertuples():
    dict[str(row.paper_id)]['authors'].append(row.name)

for key, value in dict.items():
    data = json.dumps(value)
    put_request("http://localhost:5002/papers", data.encode())
