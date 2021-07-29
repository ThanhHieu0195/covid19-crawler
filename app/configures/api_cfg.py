from flask import Flask
from flask_restful import Api
from app.services import TemplateService, Covid19Service, FCMService, StaticService


class ApiConfiguration():
    def __init__(self, name):
        self.app = Flask(name)
        self.__register_api()   

    # public function
    def run(self, options):
        # self.app.run(host=options.host, port=options.port, debug=options.debug)
        self.app.run(host=options.host, port=options.port, debug=options.debug, ssl_context=('sslkey/localhost.pem', 'sslkey/localhost-key.pem'))


    # internal methods
    def __register_api(self):
        self.api = Api(self.app)
        self.api.add_resource(Covid19Service, '/covid19')
        self.api.add_resource(TemplateService, '/analytic')
        self.api.add_resource(StaticService, '/<string:filename>.js', '/<string:filename>.json')
        self.api.add_resource(FCMService, '/fcm')