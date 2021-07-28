from flask import Flask, render_template, make_response
from flask_restful import Api
from app.services import TemplateService, Covid19Service

class ApiConfiguration():
    def __init__(self, name):
        self.app = Flask(name)
        self.__register_api()

    # public function
    def run(self):
        self.app.run(port=5000, debug=True)


    # internal methods
    def __register_api(self):
        self.api = Api(self.app)
        self.api.add_resource(Covid19Service, '/covid19')
        self.api.add_resource(TemplateService, '/analytic')