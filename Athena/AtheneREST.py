import json

from bson import ObjectId
from flask import Flask, request, jsonify
from flask.json import JSONEncoder
from flask_restful import Resource, Api

from DAL.MongoDbConnector import MongoDbConnector


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)


app = Flask(__name__)
api = Api(app)
app.json_encoder = CustomJSONEncoder


class Topics(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017')

    def put(self):
        topics = request.json

        self.conn.insert_entries('SnoBall', 'topics', topics)

    def get(self):
        id = request.args.get('id')

        if id:
            query = {"id": id}
            topic = self.conn.find_entry('SnoBall', 'topics', query)

            paper_query = {"topics": {"$elemMatch": {"id":id}}}
            papers = list(self.conn.find_entries('SnoBall', 'papers', paper_query))
            topic['relpapers'] = papers
            return jsonify({"topic": topic})
        else:
            return jsonify({"result": self.conn.get_all_entries('SnoBall', 'topics')})


class References(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017')

    def put(self):
        rawreferences = request.json

        forward = {}
        backward = {}

        for ref in rawreferences:
            if ref["Source"] not in forward:
                forward[ref["Source"]] = [ref["Target"]]
            else:
                forward[ref["Source"]].append(ref["Target"])

        for ref in rawreferences:
            if ref["Target"] not in backward:
                backward[ref["Target"]] = [ref["Source"]]
            else:
                backward[ref["Target"]].append(ref["Source"])

        for paper, refs in forward.items():
            query = {"id": paper}
            update = {"$set":{"references": refs}}

            self.conn.update('SnoBall', 'papers', query, update)

        for paper, refby in backward.items():
            query = {"id": paper}
            update = {"$set":{"referencedby": refby}}

            self.conn.update('SnoBall', 'papers', query, update)


class Authors(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017')

    def get(self):
        id = request.args.get('id')
        if id:
            query = {"id": id}
            author = self.conn.find_entry('SnoBall', 'authors', query)

            paper_query = {"authors": {"$elemMatch": {"id":1249}}}
            papers = list(self.conn.find_entries('SnoBall', 'papers', paper_query))

            author['papers'] = papers
            return jsonify({"result": author})
        else:
            return jsonify({"result": self.conn.get_all_entries('SnoBall', 'authors')})

    def put(self):
        if isinstance(request.json, dict):
            self.conn.insert_entry('SnoBall', 'authors', request.json)
        else:
            self.conn.insert_entries('SnoBall', 'authors', request.json)


class Papers(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017/')

    def put(self):
        entry = request.json
        if isinstance(entry, dict):
            self.conn.insert_entry("SnoBall", "papers", entry)
        else:
            self.conn.insert_entries("SnoBall", 'papers', entry)

    def delete(self):
        self.conn.delete_collection('SnoBall', 'papers')

    def get(self):
        id = request.args.get('id')
        if id:
            query = {"id": id}
            paper = self.conn.find_entry('SnoBall', 'papers', query)

            projection = {"id":1, "title":1, "rank":1, "year":1}

            references_query = { "id": { "$in": paper["references"]}}
            referencedby_query = {"id": { "$in" : paper["referencedby"]}}


            paper["references"] = self.conn.find_entries('SnoBall', 'papers', references_query, projection)
            paper["referencedby"] = self.conn.find_entries('SnoBall', 'papers', referencedby_query, projection)

            return jsonify({"result": paper})
        else:
            return jsonify({"result": self.conn.get_all_entries('SnoBall', 'papers')})

# Example to set up restful service
api.add_resource(Authors, '/authors')
api.add_resource(Papers, '/papers')
api.add_resource(References, '/references')
api.add_resource(Topics, '/topics')

if __name__ == '__main__':
    app.run(port='5002')
