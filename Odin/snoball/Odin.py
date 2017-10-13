from flask import Flask, render_template, request
import json
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
    return paper_id

if __name__ == "__main__":
    app.run()