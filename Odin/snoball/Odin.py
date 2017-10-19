from flask import Flask, render_template, request
import json
import urllib.request
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def main():
    return render_template('index.html')

@app.route('/sendquery', methods = ['POST'])
def sendQuery():
    query_string = request.get_data().decode('utf-8')
    request_url = "http://localhost:2222/queries/simple/{0}".format(query_string)
    r = requests.get(request_url)
    return r.text

@app.route('/paper/details', methods = ['GET'])
def get_paper():
    paper_id = request.args.get('id')
    payload = {'id': paper_id}
    paper = json.loads(requests.get('http://localhost:5002/papers', params=payload).text)["result"]

    paper["paper_text"] = paper["paper_text"].replace("\n\n", "<br/>")
    paper["paper_text"] = paper["paper_text"].replace("\n", "")

    paper["hasAbstract"] = paper["abstract"] != "Abstract Missing"
    paper["hasExtractedAbstract"] = paper["gen_abstract"] != ""

    return render_template("paper-details.html", paper = paper)

@app.route('/author/details', methods = ['GET'])
def get_author():
    author_id = request.args.get('id')
    payload = {'id': author_id}
    author = json.loads(requests.get('http://localhost:5002/authors', params=payload).text)["result"]
    return render_template("author-details.html", author = author)

if __name__ == "__main__":
    app.run()


