from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from flask import Flask, Response, make_response, jsonify
from flask_restful import Api, Resource, reqparse

import ParseyPredFace

app = Flask(__name__)
api = Api(app)

class PredAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('text', type=str, required=True)
        super(PredAPI, self).__init__()

    def get(self):
        args = self.reqparse.parse_args()
        text = args['text']

        output = ParseyPredFace.parse(text)	

        return output

api.add_resource(PredAPI, '/ppf/extract')

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
