import datetime

from dateutil.relativedelta import relativedelta


class Friend:
    def __init__(self, local_id, name, date_of_birth, image, logs, friends=[]):
        self.local_id = local_id
        self.name = name
        self.logs = logs
        self.image = image
        self.friends = friends

        birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        self.age = relativedelta(now, birth_date).years
