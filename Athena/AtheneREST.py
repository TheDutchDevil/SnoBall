import json

from flask import Flask, request
from flask_restful import Resource, Api

from DAL.MongoDbConnector import MongoDbConnector


app = Flask(__name__)
api = Api(app)

class Authors(Resource):
    def get(self):
        return "Example"

class Papers(Resource):

    def __init__(self):
        self.conn  = MongoDbConnector('mongodb://localhost:27017/')

    def put(self):
        entry = request.json
        entry["Authors"] = []
        self.conn.insertEntry("SnoBall", "papers", entry)

    def delete(self):
        self.conn.deleteCollection('SnoBall', 'papers')

#Example to set up restful service
api.add_resource(Authors, '/authors')
api.add_resource(Papers, '/papers')

if __name__ == '__main__':
     app.run(port='5002')