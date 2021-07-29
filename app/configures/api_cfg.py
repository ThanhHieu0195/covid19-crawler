from flask import Flask
from flask_restful import Api
from app.services import TemplateService, Covid19Service, FCMService, StaticService
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str)
parser.add_argument('--port', type=int)
parser.add_argument('--debug', type=bool)

args = parser.parse_args()
print(args)

if args.host is None: host = '0.0.0.0'
else: host = args.host

if args.port is None: port = 331
else: port = args.port

if args.debug is None: debug = False
else: debug = args.debug

class ApiConfiguration():
    def __init__(self, name):
        self.app = Flask(name)
        self.__register_api()   

    # public function
    def run(self):
        self.app.run(host=host, port=port, debug=debug)


    # internal methods
    def __register_api(self):
        self.api = Api(self.app)
        self.api.add_resource(Covid19Service, '/covid19')
        self.api.add_resource(TemplateService, '/analytic')
        self.api.add_resource(StaticService, '/<string:filename>.js', '/<string:filename>.json')
        self.api.add_resource(FCMService, '/fcm')