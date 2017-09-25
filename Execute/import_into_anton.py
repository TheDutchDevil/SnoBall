import csv
import urllib.request
import json

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

with open("papers/papers.csv") as csvfile:
    reader = csv.DictReader(csvfile, delimiter =",", quotechar="\"")
    for row in reader:
        paper = {}
        paper["title"] = row["title"]

        if row["abstract"] != "Abstract Missing":
            paper["paperAbstract"] = row["abstract"]
        paper["paperBody"] = row["paper_text"]

        data = json.dumps(paper)

        put_request("http://localhost:2222/papers", data.encode())