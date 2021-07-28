from app.infrastructure import Covid19Dal
from flask_restful import Resource
from datetime import datetime, timedelta
import pytz

class Covid19Service(Resource):
    def get(self):
        today_data = self.gettoday_data()
        yes_data = self.getYesData()
        detail=None
        
        if 'details' in today_data[-1]:
            detail = today_data[-1]['details']
        return {
            'case_numbers': today_data[-1]['case_numbers'],
            'increase': today_data[-1]['case_numbers'] - yes_data[-1]['case_numbers'],
            'details': detail,
            'last_updated': today_data[-1]['time']
        }

    def gettoday_data(self):
        return Covid19Dal(self.__today()).data
    
    def getYesData(self):
        return Covid19Dal(self.__yesterday()).data

    def __today(self):
        tz = pytz.timezone('Asia/Ho_Chi_Minh')
        return datetime.now(tz)

    def __yesterday(self):
        return self.__today() - timedelta(days=1)