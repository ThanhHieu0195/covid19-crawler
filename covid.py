import scrapy
import datetime
from tinydb import TinyDB
from scrapy.utils.log import configure_logging  
configure_logging(install_root_handler = False) 
import datetime
import locale
from logger import Logger

# config logger
logger = Logger("covid")

# config date
locale.setlocale(locale.LC_ALL, 'vi_VN')
current=datetime.datetime.now()

# config data
db=TinyDB('db/data-%s.json' % current.strftime('%Y-%m-%d'))
covid19=db.table('covid19')

class CovidSpider(scrapy.Spider):
    name='covid19'
    start_urls  = ["https://ncov.moh.gov.vn/"]

    def parse(self, response):
        allData = response.xpath('//div[@class="row d-none d-block d-lg-none"]').xpath('//span/text()').extract()
        analytic={}
        logger.info("start process data")
        try:
            for idx in range(0, len(allData)):
                if allData[idx] == 'Việt Nam':
                    analytic['case_numbers'] = int(allData[idx+1].replace('.', ''))
                    analytic['being_treated'] = int(allData[idx+2].replace('.', ''))
                    analytic['cured'] = int(allData[idx+3].replace('.', ''))
                    analytic['dead'] = int(allData[idx+4].replace('.', ''))
                    logger.info("parsed data")
                    break
            
            if 'case_numbers' in analytic:
                analytic['time'] = int(current.strftime('%H%M'))
                covid19.insert(analytic)
        except Exception as e:
            logger.error("Got error when parse data - reason=%s" % e.args[0])

