import schedule
import time
import os

class SpiderConfigurator():
    time_run=0.2
    path='crawler/covid19_spider.py'
    is_enabled=True

    def run(self):
        print('Scheduler initialised')
        schedule.every(self.time_run).minutes.do(lambda: os.system('scrapy runspider ' + self.path))
        print('Next job is set to run at: ' + str(schedule.next_run()))
        while True:
            if self.is_enabled is False:
                break
            schedule.run_pending()
            time.sleep(1)

            
    def stop(self):
        self.is_enabled = False