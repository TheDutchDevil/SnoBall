import json

from flask import Flask, request
from flask_restful import Resource, Api

from Athena.DAL.MongoDbConnector import MongoDbConnector


app = Flask(__name__)
api = Api(app)

class Authors(Resource):

    def __init__(self):
        self.conn = MongoDbConnector('mongodb://localhost:27017')

    def get(self):
        return "Example"

    def put(self):
        self.conn.insertEntry('SnoBall', 'authors', request.json)

class Papers(Resource):

    def __init__(self):
        self.conn  = MongoDbConnector('mongodb://localhost:27017/')

    def put(self):
        self.conn.insertEntry("SnoBall", "papers", request.json)

    def delete(self):
        self.conn.deleteCollection('SnoBall', 'papers')

#Example to set up restful service
api.add_resource(Authors, '/authors')
api.add_resource(Papers, '/papers')

if __name__ == '__main__':
     app.run(port='5002')