import datetime
from dateutil.relativedelta import relativedelta

class Friend:
    def __init__(self, local_id, name, date_of_birth, logs):
        self.local_id = local_id
        self.name = name
        self.logs = logs

        self.age = relativedelta(datetime.datetime.now() - datetime.datetime.strptime(date_of_birth, '%Y-%m-%d %H:%M:%S')).year
