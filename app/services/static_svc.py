from flask.helpers import send_file
from flask_restful import Resource
from flask import make_response, render_template

class StaticService(Resource):
    def get(self, filename):
        headers = {'Content-Type': 'text/html'}
        return send_file('static/'+filename+'.js') 