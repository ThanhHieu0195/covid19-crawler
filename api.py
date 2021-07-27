from flask import Flask
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

        return {
            'case_numbers': todayData[-1]['case_numbers'],
            'increase': todayData[-1]['case_numbers'] - yesterdayData[-1]['case_numbers']
        }

api.add_resource(CovidData, '/covid19')

if __name__ == '__main__':
    app.run(debug=True)