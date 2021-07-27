from scrapy import Spider, Selector
from tinydb import TinyDB
from scrapy.utils.log import configure_logging  
configure_logging(install_root_handler = False) 
from datetime import datetime
import pytz
from logger import Logger

# config logger
logger = Logger("covid")

# config date
tz = pytz.timezone('Asia/Ho_Chi_Minh')
current = datetime.now(tz)

# config data
db=TinyDB('db/data-%s.json' % current.strftime('%Y-%m-%d'))
covid19=db.table('covid19')

class Covid19Spider(Spider):
    name='covid19'
    start_urls  = ["https://ncov.moh.gov.vn/"]

    def parse(self, response):
        summaryData = response.xpath('//div[@class="row d-none d-block d-lg-none"]').xpath('//span/text()').extract()
        detailData = response.xpath('//div[@id="sailorTableArea"]').xpath('//tr').extract()
        data=covid19.all()
        lastAnalytic=None

        if data is not None:
            lastAnalytic=data[-1]
        analytic={}
        logger.info("start process data")
        try:
            logger.info("started take summary data")
            for idx in range(0, len(summaryData)):
                if summaryData[idx] == 'Việt Nam':
                    analytic['case_numbers'] = int(summaryData[idx+1].replace('.', ''))
                    analytic['being_treated'] = int(summaryData[idx+2].replace('.', ''))
                    analytic['cured'] = int(summaryData[idx+3].replace('.', ''))
                    analytic['dead'] = int(summaryData[idx+4].replace('.', ''))
                    logger.info("parsed data")
                    break
            logger.info("finished take summary data")
            analytic['detail'] = []
            logger.info("started take detail data")
            for idx in range(len(detailData)):
                if idx == 0: continue
                region = detailData[idx]
                record_data=Selector(text=region).xpath('//td/text()').extract()
                analytic['detail'].append({
                    'region': int(record_data[0].replace('.', '')),
                    'case_numbers': int(record_data[1].replace('.', '')),
                    'today': int(record_data[2].replace('.', '')),
                    'dead': int(record_data[3].replace('.', ''))
                })
            logger.info("finished take detail data")
            if 'case_numbers' in analytic:
                analytic['time'] = int(current.strftime('%H%M'))
                covid19.insert(analytic)
                if lastAnalytic != None:
                    if analytic['case_numbers'] != lastAnalytic['case_numbers']:
                        self.pushNotice()
            logger.info("completed crawler")
        except Exception as e:
            logger.error("Got error when parse data - reason=%s" % e.args[0])
            
    def pushNotice(self):
        pass
