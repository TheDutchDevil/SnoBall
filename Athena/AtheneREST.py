from flask import Flask, Request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Authors(Resource):
    def get(self):
        return "Example"

#Example to set up restful service
api.add_resource(Authors, '/Authors')

if __name__ == '__main__':
     app.run(port='5002')