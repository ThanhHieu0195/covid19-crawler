from scrapy import Spider, Selector
from tinydb import TinyDB
from scrapy.utils.log import configure_logging  
configure_logging(install_root_handler = False) 
from datetime import datetime, timedelta
import pytz
import os 

print(os.getcwd())

from logger import Logger

# config logger
logger = Logger("covid")

# config date
tz = pytz.timezone('Asia/Ho_Chi_Minh')
current = datetime.now(tz)

# config data
db=TinyDB('db/data-%s.json' % current.strftime('%Y-%m-%d'))
covid19=db.table('covid19')


yesterday = current - timedelta(days=1)
dbYesterday=TinyDB('db/data-%s.json' % yesterday.strftime('%Y-%m-%d'))
covid19YesterdayTable=dbYesterday.table('covid19')

class Covid19Spider(Spider):
    name='covid19'
    start_urls  = ["https://ncov.moh.gov.vn/"]

    def parse(self, response):
        logger.info('started fetch data')
        detail_data = response.xpath('//div[@id="sailorTableArea"]').xpath('//tr').extract()
        data=covid19.all()
        yesterday_data=covid19YesterdayTable.all()
        last_analytic=None

        analytic={
            'case_numbers': 0,
            'increase': 0,
            'details': []
        }
        if yesterday_data is not None and len(yesterday_data) > 0:
            last_analytic=yesterday_data[-1]
            analytic['case_numbers'] = last_analytic['case_numbers']

        try:

            logger.info("started take detail data")
            numIncreases = 0
            for idx in range(len(detail_data)):
                if idx == 0: continue
                region = detail_data[idx]
                record_data=Selector(text=region).xpath('//td/text()').extract()

                numIncreases += int(record_data[2].replace('.', ''))
                analytic['details'].append({
                    'region': record_data[0],
                    'case_numbers': int(record_data[1].replace('.', '')),
                    'today': int(record_data[2].replace('.', '')),
                    'dead': int(record_data[3].replace('.', ''))
                })
            analytic['case_numbers'] += numIncreases
            analytic['increase'] += numIncreases
            logger.info("finished take detail data")

            
            if last_analytic is None or last_analytic['case_numbers'] != analytic['case_numbers']:
                analytic['time'] = int(current.strftime('%H%M'))
                covid19.insert(analytic)
                if last_analytic != None:
                    if analytic['case_numbers'] != last_analytic['case_numbers']:
                        self.pushNotice()
            else: 
                logger.warning("Analytic is old")

            logger.info("completed crawler")
        except Exception as e:
            logger.error("Got error when parse data - reason=%s" % e.args[0])
            
    def pushNotice(self):
        pass
