import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from DAL.MongoDbConnector import MongoDbConnector

app = Flask(__name__)
api = Api(app)


class Authors(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017')

    def get(self):
        return "Example"

    def put(self):
        if isinstance(request.json, dict):
            self.conn.insertEntry('SnoBall', 'authors', request.json)
        else:
            self.conn.insertEntries('SnoBall', 'authors', request.json)

class Papers(Resource):
    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017/')

    def put(self):
        entry = request.json
        if isinstance(entry, dict):
            self.conn.insertEntry("SnoBall", "papers", entry)
        else:
            self.conn.insertEntries("SnoBall", 'papers', entry)

    def delete(self):
        self.conn.delete_collection('SnoBall', 'papers')

    def get(self):
        return jsonify({"result": self.conn.get_all_entries('SnoBall', 'papers')})

# Example to set up restful service
api.add_resource(Authors, '/authors')
api.add_resource(Papers, '/papers')

if __name__ == '__main__':
    app.run(port='5002')
