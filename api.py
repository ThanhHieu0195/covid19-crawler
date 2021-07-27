from flask import Flask, render_template, make_response
from flask_restful import Api, Resource
from tinydb import TinyDB, Query
import pytz
from datetime import datetime, timedelta, date

# 
tz = pytz.timezone('Asia/Ho_Chi_Minh')
current = datetime.now(tz)
yesterday = current - timedelta(days=1)

app = Flask(__name__)
api = Api(app)

db=TinyDB('db/data-%s.json' % current.strftime('%Y-%m-%d'))
dbYesterday=TinyDB('db/data-%s.json' % yesterday.strftime('%Y-%m-%d'))
covid19Table=db.table('covid19')
covid19YesterdayTable=dbYesterday.table('covid19')

class CovidData(Resource):
    def get(self):
        todayData = covid19Table.all()
        yesterdayData = covid19YesterdayTable.all()
        detail=None
        if 'detail' in todayData[-1]:
            detail = todayData[-1]['detail']
        return {
            'case_numbers': todayData[-1]['case_numbers'],
            'increase': todayData[-1]['case_numbers'] - yesterdayData[-1]['case_numbers'],
            'details': detail
        }


class Home(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)


api.add_resource(CovidData, '/covid19')
api.add_resource(Home, '/analytic')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    # app.run(host='0.0.0.0', port=331, debug=True)