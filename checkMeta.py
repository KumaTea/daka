from datetime import datetime, timedelta


def next_deadline(deadline_str, date=None):
    if not date:
        date = datetime.now()
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y%m%d')
    deadline = datetime.strptime(
        f'{date.year}{date.month}{date.day} {deadline_str}', '%Y%m%d %H:%M')
    if date >= deadline:
        deadline += timedelta(days=1)
    return deadline


class Check:
    def __init__(self):
        self.name = ''
        self.id = 0
        self.user = 0
        self.verify = True
        self.remind = '21:00'
        self.deadline = '00:00'
        self.enabled = '1111100'
        self.since = None
        self.until = None

    # @property
    # def reminder(self):
    #     return self.remind
    #
    # @reminder.setter
    # def reminder(self, value):
    #     self.remind = value
