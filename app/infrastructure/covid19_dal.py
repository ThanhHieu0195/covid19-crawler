from tinydb import TinyDB


class Covid19Dal():
    def __init__(self, dateTime):
        self.dateTime = dateTime
        self.__connect()
        self.fetch_data()

    def __connect(self):
        self.db = TinyDB('db/data-%s.json' % self.dateTime.strftime('%Y-%m-%d'))
        self.table = self.db.table('covid19')

        
    def fetch_data(self):
        self.data = self.table.all()
        return self.data