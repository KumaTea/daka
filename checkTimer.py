from session import logger
from checkMeta import Check


class CheckTimer:
    def __init__(self):
        self.reminders = {}
        self.deadlines = {}

    def add_check(self, check: Check):
        reminder_time = check.remind
        deadline_time = check.deadline
        if reminder_time:
            if reminder_time not in self.reminders:
                self.reminders[reminder_time] = []
            self.reminders[reminder_time].append(check.id)
        if deadline_time not in self.deadlines:
            self.deadlines[deadline_time] = []
        self.deadlines[deadline_time].append(check.id)
        logger.info(f'[ckTmr]\tcheck {check.id} added')

    def del_check(self, check: Check):
        reminder_time = check.remind
        deadline_time = check.deadline
        if reminder_time:
            self.reminders[reminder_time].remove(check.id)
            if not self.reminders[reminder_time]:
                del self.reminders[reminder_time]
        self.deadlines[deadline_time].remove(check.id)
        if not self.deadlines[deadline_time]:
            del self.deadlines[deadline_time]
        logger.info(f'[ckTmr]\tcheck {check.id} deleted')

    def init(self, checks: dict):
        for check_id in checks:
            self.add_check(checks[check_id])
        logger.info('[ckTmr]\tinitialized')
