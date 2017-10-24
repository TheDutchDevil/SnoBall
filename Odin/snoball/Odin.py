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

@app.route('/topic/details', methods=['GET'])
def get_topic():
    topicid = request.args.get('id')
    payload = {'id': topicid}
    topic = json.loads(requests.get('http://localhost:5002/topics', params=payload).text)["topic"]
    topic['minoccurence'] = min(occ[1] for occ in topic['occurence_yearly'])
    topic['maxoccurence'] = max(occ[1] for occ in topic['occurence_yearly'])
    return render_template("topic-details.html", topic = topic)

@app.route('/author/rank', methods=['GET'])
def get_rank():
    rank = int(request.arge.get('rank'))
    author_total = 8356
    if rank <= author_total / 100:
        return "diamond"
    elif rank <= (author_total /100) * 5:
        return "gold"
    elif rank <= (author_total/100) * 10:
        return "silver"
    elif rank <= (author_total/100) * 25:
        return "bronze"
    return "none"

if __name__ == "__main__":
    app.run(host="0.0.0.0")


